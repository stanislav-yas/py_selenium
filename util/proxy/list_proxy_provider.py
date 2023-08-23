from proxy_provider import ProxyProvider
from p_proxy import Pproxy
import random
import requests
import time
class ListProxyProvider(ProxyProvider):
    """ProxyProvider with proxies loaded from:
        - proxy list file
        - proxy list strings
        with line format as 'schema:ip:port:login:password'
    """

    def __init__(self, proxy_list_file = None, proxy_list_strings: str = '') -> None:
        super().__init__()
        self.proxies:list[Pproxy] = []
        """Array of available proxies"""

        self.blocked_proxies:list[Pproxy] = []
        """Array of blocked (unavailable) proxies"""

        self.proxy_index = -1
        """Index of current proxy. -1 if not set yet"""

        self.LOCAL_PORT_NUM = '8880'
        if proxy_list_file is not None:
            with open(proxy_list_file) as f:
                proxy_list_strings = f.read()
        proxy_list = proxy_list_strings.splitlines()

        for string in proxy_list:
            try:
                cnt = string.count(':')
                if cnt == 2 or cnt == 4:
                    args = [self.LOCAL_PORT_NUM]
                    args += string.strip().split(':')
                    self.proxies.append(Pproxy(*args))            
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
    
    def rotate_proxy(self, random_change=False, delay=1) -> Pproxy | None:
        """Rotate proxy. 
            - If not 'random_change', then returns next available proxy
            - delay in seconds (float)
        """
        if self.proxies_count == 0: return None
        if self.proxy_index >= 0 and self.proxy is not None:
            self.proxy.stop()
            if delay > 0:
                time.sleep(delay/2)
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
        proxy = self.proxies[self.proxy_index]
        if proxy is not None:
            proxy.start()
            if delay > 0:
                time.sleep(delay/2)
        return proxy
    
    @property
    def proxy(self) -> Pproxy | None:
        """Current available proxy"""
        if  self.proxy_index < 0:
            return self.rotate_proxy()
        else:
            return self.proxies[self.proxy_index]
        
    def block_proxy(self, do_stop=True):
        """Block current proxy (move to blocked proxy list)
            - 'do_stop' - stop current proxy if True
        """
        proxy = self.proxy
        if proxy is None: return
        if do_stop:
            proxy.stop()
        self.blocked_proxies.append(proxy)
        self.proxies.remove(proxy)
        if len(self.proxies) == 0:
            self.proxy_index = -1        
        elif self.proxy_index >= len(self.proxies):
            self.proxy_index = 0

        
    def check_proxy(self, check_type=0, timeout=10) -> bool:
        """Checking availability of current proxy at https://httpbin.org/ip """
        proxy = self.proxy
        if proxy is None: return False
        proxies = {
            # 'http': f'http://{proxy_url}',
            # 'https': f'https://{proxy_url}',
            # 'http': f'socks5://{proxy_url}',
            # 'https': f'socks5://{proxy_url}',
            'all': f'{proxy.scheme}://localhost:{proxy.lport}',          
        }
        try:
            proxy.start()
            print(f'Checking proxy: {proxy}...')
            
            if check_type == 0:
                check_site_url = 'https://api.myip.com/'
            else:
                check_site_url = 'https://httpbin.org/ip'
            response = requests.get(check_site_url, proxies=proxies, verify=True, timeout=timeout)
            print(f'Checking elapsed {response.elapsed.seconds} seconds, status_code = {response.status_code}')
            if response.status_code == requests.codes.ok:
                if check_type == 0:
                    origin = response.json()['ip']
                else:
                    origin = response.json()['origin']
                if origin == proxy.host:
                    print(f'Checking success, proxy: {proxy.host}, origin: {origin}')
                    return True
                else:
                    print(f'Checking failed, proxy: {proxy.host}, origin: {origin}')
                    return False
        except Exception as err:
            print(err)
        print('Checking failed')
        return False
    
    def __repr__(self) -> str:
        return f"ListProxyProvider (proxies: {len(self.proxies)+len(self.blocked_proxies)}, blocked: {len(self.blocked_proxies)}, current: {self.proxy})"

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