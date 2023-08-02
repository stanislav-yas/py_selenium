class Proxy:
    UNKNOWN_TYPE = 0
    LIST_PROXY_TYPE = 1
    API_PROXY_TYPE = 2
    
class ProxyProvider:
    def __init__(self) -> None:
        type = Proxy.UNKNOWN_TYPE