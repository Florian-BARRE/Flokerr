from configuration import APP_CONFIG

# Websocket library
import aiohttp

# Database library
import database as db_module

# server tools
import server.tools as server_tools

# WS tools / class
from server.ws.ws_class import WebSocketClient
import server.ws.tools as ws_tools

# Import all endpoints
import server.ws.endpoints as ws_endpoints

# Import ws client pinger, it's need to be started as a background task
from server.ws.tools import ping_ws_clients


# Create the websocket handler from all endpoints
async def websocket_handler(request):
    ws_obj = WebSocketClient(aiohttp.web.WebSocketResponse(protocols=['arduino']))
    await ws_obj.ws.prepare(request)
    APP_CONFIG.GLOBAL["ws_clients_set"].add(ws_obj)

    server_tools.dprint("New user connected", 1)
    server_tools.dprint(f"New user uuid: {ws_obj.id}", 2)
    server_tools.dprint(f"Total users: {len(APP_CONFIG.GLOBAL['ws_clients_set'])}", 2)

    try:
        async for msg in ws_obj.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                # WS is most used by IoT devices, so we want to get the name of the requester device
                # We can get it from the 'infos' key in the payload
                # If the 'infos' key is not provided, we use the UUID as name
                ws_infos = APP_CONFIG.GLOBAL["ws_clients_registry"].get(ws_obj.id, {}).get("infos", {})
                ws_name = ws_infos.get("name", ws_obj.id)

                # Get the request in JSON type
                request = server_tools.decode_request(msg.data)

                # If the request is not valid, send an error message
                if request.get("status_code") == APP_CONFIG.CODE_ERROR["crash"]:
                    await ws_obj.ws.send_json(request)
                    server_tools.dprint(f"New request received: user[{ws_name}], request is not valid ! [{request}]", 1)
                    continue

                server_tools.dprint(f"New request received: user[{ws_name}]", 1)

                # Get the request type
                request_type = request.get("type")
                server_tools.dprint(f"Request type: [{request_type}], payload[{request}]", 2)

                # If the request is an authentication request, handle it, without authenticated restrictions
                if request_type in ["auth", "authenticate", "authentication"]:
                    await ws_obj.ws.send_json(
                        await ws_endpoints.authentication_handler(request, ws_obj)
                    )
                    continue

                # Check if the client is already authenticated
                if APP_CONFIG.GLOBAL["ws_clients_registry"].get(ws_obj.id, None) is None:
                    # If the request is not an authentication request, send an error message
                    await ws_obj.ws.send_json(
                        {"status": "You are not authenticated", "status_code": APP_CONFIG.CODE_ERROR["unauthorize"]}
                    )
                    continue

                # If the client is authenticated, check the client privileges
                client_auth_infos = APP_CONFIG.GLOBAL["ws_clients_registry"].get(ws_obj.id)

                # Check the user authorization
                is_authorize = server_tools.check_authorization(client_auth_infos.get("privileges"), request_type)

                if not is_authorize:
                    await ws_obj.ws.send_json(
                        {"status": "You are not authorize to perform this action",
                         "status_code": APP_CONFIG.CODE_ERROR["unauthorize"]}
                    )
                    server_tools.dprint(f"[{ws_name}] as not enough privileges to perform this action !", 3)
                    continue

                # Client authenticated and have enough privileges let's perform its request
                with db_module.app.app_context():

                    if request_type == "write":
                        await ws_obj.ws.send_json(
                            await ws_endpoints.write_handler(request, ws_obj)
                        )

                    elif request_type == "read":
                        await ws_obj.ws.send_json(
                            await ws_endpoints.read_handler(request, ws_obj)
                        )

                    elif request_type == "delete":
                        await ws_obj.ws.send_json(
                            await ws_endpoints.delete_handler(request, ws_obj)
                        )

                    elif request_type == "ping_ws_device":
                        await ws_obj.ws.send_json(
                            await ws_endpoints.ping_ws_device_handler(request, ws_obj)
                        )

                    elif request_type == "subscribe":
                        await ws_obj.ws.send_json(
                            await ws_endpoints.subscribe_handler(request, ws_obj)
                        )

                    elif request_type == "unsubscribe":
                        await ws_obj.ws.send_json(
                            await ws_endpoints.unsubscribe_handler(request, ws_obj)
                        )

                    elif request_type == "multi":
                        await ws_obj.ws.send_json(
                            await ws_endpoints.multi_handler(request, ws_obj)
                        )

    finally:
        ws_infos = APP_CONFIG.GLOBAL["ws_clients_registry"].get(ws_obj.id, {}).get("infos", {})
        ws_name = ws_infos.get("name", ws_obj.id)

        ws_tools.clear_ws_client(ws_obj)
        server_tools.dprint("User disconnected", 1)
        server_tools.dprint(f"Old user name or uuid: {ws_name}", 2)
        server_tools.dprint(f"Total users: {len(APP_CONFIG.GLOBAL['ws_clients_set'])}", 2)

    return ws_obj.ws
