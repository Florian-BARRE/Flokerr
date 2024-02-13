from configuration import APP_CONFIG

import os
import asyncio

import database as db_module

from server.ws.endpoints.authentication import authentication_handler
from server.ws.endpoints.delete import delete_handler
from server.ws.endpoints.ping_ws_device import ping_ws_device_handler
from server.ws.endpoints.read import read_handler
from server.ws.endpoints.subscribe import subscribe_handler
from server.ws.endpoints.unsubscribe import unsubscribe_handler
from server.ws.endpoints.write import write_handler

import server.tools as server_tools


async def multi_task(tasks, client_privileges, ws_client=None):
    """
    This function is used to handle multiple requests in one call using asyncio.
    :param tasks: a list with all tasks to perform
    :param client_privileges: it will be used to check if the client has enough privileges to perform the task
    :param ws_client: is None by default, but if it is not, it means that the client is connected to the websocket,
    so it can perform some actions that are not allowed in HTTP
    :return:
    """
    try:
        if tasks is None or len(tasks) == 0:
            return {"status": "'requests' parameter is missing or incorrect",
                    "status_code": APP_CONFIG.CODE_ERROR["missing_parameter"]}

        # Execute the task concurrently, a task_selector is async function
        tasks_results = await asyncio.gather(
            *(task_selector(task, client_privileges, ws_client) for task in tasks),
            return_exceptions=True
        )

        # Add the results to a list
        results = [result for result in tasks_results]

        return {
            "results": results,
            "status": APP_CONFIG.STATUS["multi"]["success"],
            "status_code": APP_CONFIG.CODE_ERROR["success"]
        }

    except Exception as e:
        return {"status": APP_CONFIG.STATUS["multi"]["fail"], "error_message": str(e),
                "status_code": APP_CONFIG.CODE_ERROR["crash"]}



async def task_selector(task, client_privileges, ws_client=None):
    """
    This function is used to select the right handler for the task
    and check if the client has enough privileges to perform the task
    :param task:
    :param client_privileges:
    :param ws_client:
    :return:
    """
    request_type = task.get("type", None)

    # Check if the client has enough privileges to perform this action
    is_authorize = server_tools.check_authorization(client_privileges, request_type)
    if not is_authorize:
        return {
            "status": "You are not authorize to perform this action",
            "status_code": APP_CONFIG.CODE_ERROR["unauthorize"]
        }

    # If the client is authorized, perform the request
    with db_module.app.app_context():
        if request_type == "authentication" and ws_client is not None:
            return await authentication_handler(task, ws_client)
        elif request_type == "delete":
            return await delete_handler(task)
        elif request_type == "ping_ws_device":
            return await ping_ws_device_handler(task)
        elif request_type == "read":
            return await read_handler(task)
        elif request_type == "subscribe" and ws_client is not None:
            return await subscribe_handler(task, ws_client)
        elif request_type == "unsubscribe" and ws_client is not None:
            return await unsubscribe_handler(task, ws_client)
        elif request_type == "write":
            return await write_handler(task)
        else:
            return {"status": "Unknown action", "status_code": APP_CONFIG.CODE_ERROR["unauthorize"]}
