from configuration import APP_CONFIG

from server.tools import research_ws_device


def ping_ws_device_task(uuid, name):
    """
    This function is used to ping a ws device. We can provide the uuid or the name of the device.
    It will search in the registery if the device is connected or not.
    UUID is the priority (it's unique).
    If multiple devices are found (resarch by name), a list of devices is returned.
    :param uuid:
    :param name:
    :return:
    """
    try:
        device_infos, devices_count = research_ws_device(uuid, name)

        # If no device is found, it means that the device is not connected
        if device_infos is None:
            return {
                "status": APP_CONFIG.STATUS["ping_ws_device"]["success"],
                "infos": "null",
                "connected": False,
                "devices_count": devices_count,  # It should always be 0
                "status_code": APP_CONFIG.CODE_ERROR["success"]
            }

        # If the device is found, it means that the device is connected
        return {
            "status": APP_CONFIG.STATUS["ping_ws_device"]["success"],
            "infos": device_infos,
            "connected": True,
            "devices_count": devices_count,  # It should always be 0
            "status_code": APP_CONFIG.CODE_ERROR["success"]
        }

    except Exception as e:
        return {"status": APP_CONFIG.STATUS["ping_ws_device"]["fail"], "error_message": str(e),
                "status_code": APP_CONFIG.CODE_ERROR["crash"]}
