from proxy_provider import Proxy, ProxyProvider
import random

class ListProxyProvider(ProxyProvider):
    type = Proxy.LIST_PROXY_TYPE
    ''' Pool of proxies
    '''
    _pool = []
    _index = -1

    def __init__(self, proxy_list_str: str = '') -> None:
        super().__init__()
        proxy_list = proxy_list_str.splitlines()
        for proxy in proxy_list:
            try:
                ip, port = proxy.split(':', 2)
            except:
                continue
            self._pool.append([ip, port])
        if len(self._pool) == 0:
            raise Exception('Empty proxy pool')     
    
    def next_proxy(self, is_random = False) -> list:
        prev_index = self._index
        if is_random and len(self._pool) > 2:
            index = prev_index
            while index == prev_index:
                index = random.randrange(len(self._pool))
            self._index = index
        else:
            self._index += 1
            if self._index >= len(self._pool):
                self._index = 0            
        return self._pool[self._index]

sample_proxy_list_str = '''
82.145.46.190:3128
132.145.57.78:80
89.116.229.56:80
141.170.28.103:8080
46.17.63.166:18888
'''

if __name__ == '__main__' :
    provider = ListProxyProvider(proxy_list_str=sample_proxy_list_str)
    print(provider.next_proxy())
    print(provider.next_proxy())
    print(provider.next_proxy(is_random=True))
    print(provider.next_proxy(is_random=True))
    print(provider.next_proxy())
    print(provider.next_proxy())
    print(provider.next_proxy())
    print(provider.next_proxy())
    print(provider.next_proxy())    