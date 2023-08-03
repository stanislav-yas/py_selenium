from proxy_provider import Proxy, ProxyProvider
import random
import requests
class ListProxyProvider(ProxyProvider):

    def __init__(self, proxy_list_str: str = '') -> None:
        super().__init__()
        self.type = Proxy.LIST_PROXY_TYPE
        self.proxies = []
        '''Array of available proxies. Proxy is an array of [ip, port, login. password]'''        
        self.blocked_proxies = []
        '''Array of blocked (unavailable) proxies'''
        self.proxy_index = -1
        '''Index of current proxy. -1 if not set yet '''        
        proxy_list = proxy_list_str.splitlines()
        for proxy in proxy_list:
            try:
                cnt = proxy.count(':')
                if cnt == 1 or cnt == 3:
                    self.proxies.append(proxy.strip().split(':'))            
            except:
                 continue          
        if len(self.proxies) == 0:
            raise Exception('Empty proxy pool')    

    @property
    def proxies_count(self):
        return len(self.proxies)
    
    @property
    def all_proxies(self):
        '''All proxies including blocked'''
        return self.proxies + self.blocked_proxies
    
    def change_proxy(self, random_change = False) -> list | None:
        '''Change proxy. If not 'random_change' then returns next available proxy'''
        if(self.proxies_count == 0): return None
        prev_index = self.proxy_index
        if random_change and len(self.proxies) > 2:
            index = prev_index
            while index == prev_index:
                index = random.randrange(len(self.proxies))
            self.proxy_index = index
        else:
            self.proxy_index += 1
            if self.proxy_index >= len(self.proxies):
                self.proxy_index = 0            
        return self.proxies[self.proxy_index]
    
    @property
    def proxy(self) -> list | None:
        '''Current available proxy'''
        if  self.proxy_index < 0:
            return self.change_proxy()
        else:
            return self.proxies[self.proxy_index]
        
    def block_proxy(self):
        '''Block current proxy (move to blocked proxy list)'''
        self.blocked_proxies.append(self.proxy)
        self.proxies.remove(self.proxy)
        if len(self.proxies) == 0:
            self.proxy_index = -1        
        elif self.proxy_index >= len(self.proxies):
            self.proxy_index = 0

        
    def check_proxy(self, timeout=10) -> bool:
        proxy = self.proxy
        if proxy == None: return False
        if len(proxy) >= 4:
            proxy_url = f'{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}'
        elif len(proxy) >= 2:
            proxy_url = f'{proxy[0]}:{proxy[1]}'
        else: return False
        proxies = {
            # 'http': f'http://{proxy_url}',
            # 'https': f'https://{proxy_url}',
            # 'http': f'socks5://{proxy_url}',
            # 'https': f'socks5://{proxy_url}',
            'all': f'socks5://{proxy_url}',          
        }
        try:
            print(f'Checking proxy: {proxy}...')
            response = requests.get('https://httpbin.org/ip', proxies=proxies, verify=True, timeout=timeout)
            print(f'Checking elapsed {response.elapsed.seconds} seconds, status_code = {response.status_code}')
            if response.status_code == requests.codes.ok:
                origin = response.json()['origin']
                if origin == proxy[0]:
                    print(f'Checking success, origin {origin}')
                    return True
                else:
                    print(f'Checking failed, origin {origin}')
                    return False
        except Exception as err:
            print(err)
        print('Checking failed')
        return False
    
    def __repr__(self) -> str:
        return f"ListProxyProvider (proxies: {len(self.proxies)+len(self.blocked_proxies)}, blocked: {len(self.blocked_proxies)}, current: {self.proxy})"

sample_proxy_list_str = '''
#gjgjfgsjfh
109.172.113.130:59101:staniaskz:WiRhdJv7ty
93.188.207.49:59101:staniaskz:WiRhdJv7ty	
212.8.229.77:59101:staniaskz:WiRhdJv7ty	
77.83.118.44:59101:staniaskz:WiRhdJv7ty
94.137.90.126:59101:staniaskz:WiRhdJv7ty
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
    pp1 = ListProxyProvider(proxy_list_str=sample_proxy_list_str)
    print(pp1)
    # pp2 = ListProxyProvider(proxy_list_str=sample_proxy_list_str2)
    for proxy in pp1.all_proxies:
        if not pp1.check_proxy():
            pp1.block_proxy()
        else:
            pp1.change_proxy()
    print(pp1)
    # print(pp1.next_proxy())
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