from abc import ABC

class ProxyProvider(ABC):

    def rotate_proxy(self, random_change = False) -> list | None:
        raise NotImplemented