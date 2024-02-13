from configuration import APP_CONFIG

from server.decorators import parse_response, stopwatch
from server.ws.decorators import activity_tracker

from server.commons_endpoints.multi import multi_task


@parse_response()
@activity_tracker()
@stopwatch()
async def multi_handler(payload, client):
    client_auth_infos = APP_CONFIG.GLOBAL["ws_clients_registry"].get(client.id)

    # Get all params
    tasks = payload.get("tasks", None)

    return await multi_task(
        tasks,
        client_auth_infos.get("privileges"),
        client
    )
