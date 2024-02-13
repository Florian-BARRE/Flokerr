from configuration import APP_CONFIG

import asyncio

import server.tools as server_tools
from server.ws.ws_class import WebSocketClient


def get_client_from_id(client_id) -> WebSocketClient:
    """
    This function returns the ws client object from its UUID / ID.
    It allows to get native ws object from an ID.

    * When a new ws client connect to the server, it is automatically add to ws_clients_set.
    :param client_id:
    :return:
    """
    for client in APP_CONFIG.GLOBAL["ws_clients_set"]:
        if client.id == client_id:
            return client


def delete_client_subscription_from_id(client_id):
    """
    This function deletes a client from all topics subscribed.
    It can be used when the client disconnects.
    :param client_id:
    :return:
    """
    i = 0
    while i < len(APP_CONFIG.GLOBAL["ws_subscriptions"]):
        if APP_CONFIG.GLOBAL["ws_subscriptions"][i]['client_id'] == client_id:
            del APP_CONFIG.GLOBAL["ws_subscriptions"][i]
        else:
            i += 1


def clear_ws_client(client_obj: WebSocketClient):
    """
    This function deletes a ws client from
     - ws_clients_registry (list with all authenticated clients and their infos
     - ws_clients_set (set with all connected clients)
    :param client_obj:
    :return:
    """
    # Remove the client from the subscriptions / registry / infos / set
    try:
        delete_client_subscription_from_id(client_obj.id)
        APP_CONFIG.GLOBAL["ws_clients_registry"].pop(client_obj.id, None)
        APP_CONFIG.GLOBAL["ws_clients_set"].remove(client_obj)
    except Exception as error:
        server_tools.dprint(f"Error during client deletion: {error}", 1)
        server_tools.dprint(f"Client ID: {client_obj.id}", 2)
        server_tools.dprint(f"Set of all client id: {[client.id for client in APP_CONFIG.GLOBAL['ws_clients_set']]}", 3)

async def ping_ws_clients():
    """
    This function pings all current clients connected.
    If one doesn't respond,
     - Its server's connection will be closed
     - It will be clear from the server.
    :return:
    """
    while True:
        disconnected_clients = []

        for ws_obj in APP_CONFIG.GLOBAL["ws_clients_set"]:
            ping_duration = "not found"

            try:
                start_time = asyncio.get_event_loop().time()
                await ws_obj.ws.ping()
                end_time = asyncio.get_event_loop().time()
                ping_duration = round((end_time - start_time) * 1000, 4)
                # Add ping duration to device info
                APP_CONFIG.GLOBAL["ws_clients_registry"][ws_obj.id]["infos"]["ping"] = ping_duration

            except Exception as error:
                ws_infos = APP_CONFIG.GLOBAL["ws_clients_registry"].get(ws_obj.id, {}).get("infos", {})
                ws_name = ws_infos.get("name", ws_obj.id)

                server_tools.dprint(
                    f"Pinging [{ws_name}] device failed, disconnecting it from the server. ({error})", 1)
                disconnected_clients.append(ws_obj)

        for ws_obj in disconnected_clients:
            clear_ws_client(ws_obj)

        await asyncio.sleep(APP_CONFIG.PING_WS_CLIENTS_INTERVAL)
