from configuration import APP_CONFIG

import aiohttp
import asyncio

import server.ws as ws
import server.http as http

# Create the application
app = aiohttp.web.Application(debug=True)

# WebSocket endpoint definition
app.router.add_get(f'{APP_CONFIG.API_ROOT}{APP_CONFIG.WS_PATH}', ws.websocket_handler)

# HTTP endpoints definition
app.router.add_get(f'{APP_CONFIG.API_ROOT}{APP_CONFIG.HTTP_PATH}/auth', http.authentication_handler)
app.router.add_get(f'{APP_CONFIG.API_ROOT}{APP_CONFIG.HTTP_PATH}/read', http.read_handler)
app.router.add_get(f'{APP_CONFIG.API_ROOT}{APP_CONFIG.HTTP_PATH}/write', http.write_handler)
app.router.add_get(f'{APP_CONFIG.API_ROOT}{APP_CONFIG.HTTP_PATH}/delete', http.delete_handler)
app.router.add_get(f'{APP_CONFIG.API_ROOT}{APP_CONFIG.HTTP_PATH}/ping_ws_device', http.ping_ws_device_handler)
app.router.add_post(f'{APP_CONFIG.API_ROOT}{APP_CONFIG.HTTP_PATH}/multi', http.multi_handler)


# Background tasks
async def start_background_tasks(current_app):
    current_app['ping_task'] = asyncio.create_task(ws.ping_ws_clients())


# Start the application
app.on_startup.append(start_background_tasks)
