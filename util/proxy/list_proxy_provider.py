from proxy_provider import Proxy, ProxyProvider
import random
import requests
class ListProxyProvider(ProxyProvider):
    type = Proxy.LIST_PROXY_TYPE
    _pool = []
    '''Pool of proxies. Proxy is an array of [ip, port]'''
    _index = -1
    '''Index of current proxy. -1 if not set yet '''

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

    @property
    def proxies_count(self):
        return len(self._pool)
    
    @property
    def all_proxies(self):
        return self._pool
    
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
    
    def current_proxy(self) -> list:
        if  self._index < 0:
            return self.next_proxy()
        else:
            return self._pool[self._index]
        
    def check_proxy(self) -> bool:
        proxy = self.current_proxy()
        proxies = {
            'http': f'http://{proxy[0]}:{proxy[1]}',
            'https': f'https://{proxy[0]}:{proxy[1]}',
        }
        try:
            print(f'Trying proxy: {proxy[0]}:{proxy[1]}...')
            response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
            if response.status_code == requests.codes.ok:
                origin = response.json()['origin']
                print(f'Result = {response.status_code}, Response elapsed {response.elapsed.seconds} seconds, origin={origin}')
                return True
            else:
                print(f'Result = {response.status_code}, failed')
        except Exception as err:
            print(err)       
        return False

sample_proxy_list_str = '''
82.145.46.190:3128
132.145.57.78:80
89.116.229.56:80
141.170.28.103:8080
46.17.63.166:18888
'''

if __name__ == '__main__' :
    pp1 = ListProxyProvider(proxy_list_str=sample_proxy_list_str)
    for proxy in pp1.all_proxies:
        pp1.next_proxy()
        print(pp1.check_proxy())
    # print(pp1.next_proxy())
    pass
    # print(pp1.next_proxy(is_random=True))
    # pp1.check_proxy()
    # print(pp1.next_proxy(is_random=True))
    # pp1.check_proxy()
    # print(pp1.next_proxy())
    # print(pp1.next_proxy())
    # print(pp1.next_proxy())
    # pp2 = ListProxyProvider(proxy_list_str=sample_proxy_list_str)
    # print(pp1.current_proxy())
    # print(pp2.current_proxy())
    pass