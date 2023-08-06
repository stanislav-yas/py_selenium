from proxy_provider import Proxy, ProxyProvider
import random
import requests
class ListProxyProvider(ProxyProvider):
    """ProxyProvider with proxies loaded from:
        - proxy list file
        - proxy list strings
    """

    def __init__(self, proxy_list_file = None, proxy_list_strings: str = '') -> None:
        super().__init__()
        self.type = Proxy.LIST_PROXY_TYPE
        self.proxies = []
        """Array of available proxies. Proxy is an array of [protocol, ip, port, login. password]"""

        self.blocked_proxies = []
        """Array of blocked (unavailable) proxies"""

        self.proxy_index = -1
        """Index of current proxy. -1 if not set yet"""

        if proxy_list_file != None:
            with open(proxy_list_file) as f:
                proxy_list_strings = f.read()
        proxy_list = proxy_list_strings.splitlines()

        for proxy in proxy_list:
            try:
                cnt = proxy.count(':')
                if cnt == 2 or cnt == 4:
                    self.proxies.append(proxy.strip().split(':'))            
            except:
                continue          
        if len(self.proxies) == 0:
            raise Exception('ListProxyProvider creation failed - proxies absent')    

    @property
    def proxies_count(self):
        """Count of the available proxies"""
        return len(self.proxies)
    
    @property
    def all_proxies(self):
        '''All proxies including blocked'''
        return self.proxies + self.blocked_proxies
    
    def rotate_proxy(self, random_change = False) -> list | None:
        """Rotate proxy. If not 'random_change', then returns next available proxy"""
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
        """Current available proxy"""
        if  self.proxy_index < 0:
            return self.rotate_proxy()
        else:
            return self.proxies[self.proxy_index]
        
    def block_proxy(self):
        """Block current proxy (move to blocked proxy list)"""
        self.blocked_proxies.append(self.proxy)
        self.proxies.remove(self.proxy)
        if len(self.proxies) == 0:
            self.proxy_index = -1        
        elif self.proxy_index >= len(self.proxies):
            self.proxy_index = 0

        
    def check_proxy(self, timeout=10) -> bool:
        """Checking availability of current proxy at https://httpbin.org/ip """
        proxy = self.proxy
        if proxy == None: return False
        if len(proxy) >= 5:
            proxy_url = f'{proxy[3]}:{proxy[4]}@{proxy[1]}:{proxy[2]}'
        elif len(proxy) >= 3:
            proxy_url = f'{proxy[1]}:{proxy[2]}'
        else: return False
        proxies = {
            # 'http': f'http://{proxy_url}',
            # 'https': f'https://{proxy_url}',
            # 'http': f'socks5://{proxy_url}',
            # 'https': f'socks5://{proxy_url}',
            'all': f'{proxy[0]}://{proxy_url}',          
        }
        try:
            print(f'Checking proxy: {self.proxy_str}...')
            response = requests.get('https://httpbin.org/ip', proxies=proxies, verify=True, timeout=timeout)
            print(f'Checking elapsed {response.elapsed.seconds} seconds, status_code = {response.status_code}')
            if response.status_code == requests.codes.ok:
                origin = response.json()['origin']
                if origin == proxy[1]:
                    print(f'Checking success, origin: {origin}')
                    return True
                else:
                    print(f'Checking failed, origin: {origin}')
                    return False
        except Exception as err:
            print(err)
        print('Checking failed')
        return False
    
    @property
    def proxy_str(self):
        """String representation of proxy, w/o login,pwd"""
        return f'{self.proxy[0]}//{self.proxy[1]}:{self.proxy[2]}' if self.proxy != None else None
    
    def __repr__(self) -> str:
        return f"ListProxyProvider (proxies: {len(self.proxies)+len(self.blocked_proxies)}, blocked: {len(self.blocked_proxies)}, current: {self.proxy_str})"

socks5_proxy_list_str = '''
#shdgfsjhgjfgdjh
socks5:94.137.90.126:59101:staniaskz:WiRhdJv7ty	
socks5:109.172.113.130:59101:staniaskz:WiRhdJv7ty	
socks5:93.188.207.49:59101:staniaskz:WiRhdJv7ty	
socks5:212.8.229.77:59101:staniaskz:WiRhdJv7ty	
socks5:77.83.118.44:59101:staniaskz:WiRhdJv7ty	
'''

if __name__ == '__main__' :
    # pp1 = ListProxyProvider(proxy_list_strings=socks5_proxy_list_str)
    pp1 = ListProxyProvider(proxy_list_file='util/proxy/proxy_list.txt')
    print(pp1)
    for i in range(0, pp1.proxies_count):
        if not pp1.check_proxy():
            pp1.block_proxy()
        else:
            pp1.rotate_proxy()
    print(pp1)
    pass