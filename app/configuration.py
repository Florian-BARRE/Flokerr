import json
import os


def load_json_file(file_path):
    try:
        with open(file_path) as config:
            file_json = json.load(config)
    except FileNotFoundError:
        try:
            with open(os.path.join(BASE_DIR, file_path)) as config:
                file_json = json.load(config)
        except Exception:
            raise

    return file_json


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

SECRET_CONFIG_STORE = load_json_file("secrets.json")
CONFIG_STORE = load_json_file("configuration.json")


class Config:
    # General
    APPLICATION_NAME = 'Flokerr'
    BASE_DIR = BASE_DIR
    GLOBAL = {
        "ws_clients_set": set(),
        "ws_clients_registry": dict(),
        "ws_subscriptions": list(),
    }

    CODE_ERROR = {
        "success": 200,
        "unauthorize": 401,
        "missing_parameter": 400,
        "crash": 500
    }

    STATUS = {
        "read": {"success": "topic's reader works successfully.", "fail": "topic's reader works unsuccessfully."},
        "write": {"success": "topic's writer works successfully.", "fail": "topic's writer works unsuccessfully."},
        "delete": {"success": "topic's deleter works successfully.", "fail": "topic's deleter works unsuccessfully."},
        "ping_ws_device": {"success": "ws device pinger works successfully.",
                           "fail": "ws device pinger works unsuccessfully."},

        "subscribe": {"success": "topic's subscriber works successfully.",
                      "fail": "topic's subscriber works unsuccessfully. "},
        "unsubscribe": {"success": "topic's unsubscriber works successfully.",
                        "fail": "topic's unsubscriber works unsuccessfully. "},

        "multi": {"success": "multi tasks executer works successfully.",
                  "fail": "multi tasks executer works unsuccessfully."},

        "decode_request": {"success": "", "fail": "Error during decoding payload process."},
        "get_authentification_token": {"success": "", "fail": "Error during getting token info process."},

        "authentication": {"success": "Your have been successfully authenticated.",
                           "fail": "Error during authentication process."},
    }

    # Get configuration from docker compose env variables (use for production deployment)
    # Or from config files (use for development)

    # Secret config
    if os.getenv('DB_USER', None) is not None and os.getenv('DB_PASSWORD', None) is not None \
        and os.getenv('DB_HOST', None) is not None and os.getenv(
            'DB_NAME', None) is not None:
        FLOKER_CONN_STR = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(
            os.getenv('DB_USER', 'root'),
            os.getenv('DB_PASSWORD', ''),
            os.getenv('DB_HOST', 'localhost'),
            os.getenv('DB_NAME', 'flokerr')
        )
    else:
        FLOKER_CONN_STR = SECRET_CONFIG_STORE["floker_conn_str"]

    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', SECRET_CONFIG_STORE["encryption_key"])
    CREDENTIALS = os.getenv('CREDENTIALS', SECRET_CONFIG_STORE["credentials"])

    # Config
    LISTENING_PORT = int(os.getenv('LISTENING_PORT', CONFIG_STORE["listening_port"]))
    API_ROOT = os.getenv('API_ROOT', CONFIG_STORE["API_root"])
    WS_PATH = os.getenv('WS_PATH', CONFIG_STORE["WS_path"])
    HTTP_PATH = os.getenv('HTTP_PATH', CONFIG_STORE["HTTP_path"])
    PING_WS_CLIENTS_INTERVAL = int(os.getenv('PING_WS_CLIENTS_INTERVAL', CONFIG_STORE["ping_ws_clients_interval"]))
    HISTORY_TOPIC_TABLE_BASE_NAME = os.getenv('HISTORY_TOPIC_TABLE_BASE_NAME',
                                              CONFIG_STORE["history_topic_table_base_name"])
    DEFAULT_HISTORY_SIZE = int(os.getenv('DEFAULT_HISTORY_SIZE', CONFIG_STORE["default_history_size"]))
    WARNING_THRESHOLD_TIME = int(os.getenv('WARNING_TRESHOLD_TIME', CONFIG_STORE["warning_treshold_time"]))
    PRIORITY_DEBUG_LEVEL = int(os.getenv('PRIORITY_DEBUG_LEVEL', CONFIG_STORE["priority_debug_level"]))


class Configuration(dict):

    def from_object(self, obj):
        for attr in dir(obj):

            if not attr.isupper():
                continue

            self[attr] = getattr(obj, attr)

        self.__dict__ = self


APP_CONFIG = Configuration()
APP_CONFIG.from_object(Config)
