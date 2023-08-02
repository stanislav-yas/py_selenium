from proxy_provider import Proxy, ProxyProvider
import random
import requests
from requests.auth import HTTPDigestAuth, HTTPBasicAuth, HTTPProxyAuth
class ListProxyProvider(ProxyProvider):

    def __init__(self, proxy_list_str: str = '') -> None:
        super().__init__()
        self.type = Proxy.LIST_PROXY_TYPE
        self._pool = []
        '''Pool of proxies. Proxy is an array of [ip, port]'''
        self._index = -1
        '''Index of current proxy. -1 if not set yet '''        
        proxy_list = proxy_list_str.splitlines()
        for proxy in proxy_list:
            try:
                cnt = proxy.count(':')
                if cnt == 1 or cnt == 3:
                    self._pool.append(proxy.strip().split(':'))            
            except:
                 continue          
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
        if len(proxy) >= 4:
            proxy_url = f'{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}'
        elif len(proxy) >= 2:
            proxy_url = f'{proxy[0]}:{proxy[1]}'
        else: return False
        proxies = {
            'http': f'http://{proxy_url}',
            'https': f'https://{proxy_url}',
        }
        try:
            print(f'Trying proxy: {proxy}...')
            # response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
            auth = HTTPBasicAuth('staniaskz', 'WiRhdJv7ty')
            response = requests.get('https://httpbin.org/ip', proxies=proxies, auth=auth, verify=False, timeout=10)
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
#gjgjfgsjfh
94.137.90.126:59100:staniaskz:WiRhdJv7ty
109.172.113.130:59100:staniaskz:WiRhdJv7ty
93.188.207.49:59100:staniaskz:WiRhdJv7ty	
212.8.229.77:59100:staniaskz:WiRhdJv7ty	
77.83.118.44:59100:staniaskz:WiRhdJv7ty	
'''
sample_proxy_list_str2 = '''
#shdgfsjhgjfgdjh
94.137.90.126:59100
109.172.113.130:59100
93.188.207.49:59100	
212.8.229.77:59100
77.83.118.44:59100
'''

if __name__ == '__main__' :
    pp1 = ListProxyProvider(proxy_list_str=sample_proxy_list_str2)
    # pp2 = ListProxyProvider(proxy_list_str=sample_proxy_list_str2)
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