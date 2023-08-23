from abc import ABC

class ProxyProvider(ABC):

    def rotate_proxy(self, random_change=False, delay=0) -> list | None:
        raise NotImplemented