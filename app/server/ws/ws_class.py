import uuid


class WebSocketClient:
    """
    This class contain the native websocket client of the
    aiohttp librairy with an additional UUID.
    """
    def __init__(self, ws):
        self.ws = ws
        self.id = str(uuid.uuid4())

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id
