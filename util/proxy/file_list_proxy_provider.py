from list_proxy_provider import ListProxyProvider

class FileListProxyProvider(ListProxyProvider):
    '''ProxyProvider created from proxy list file'''

    def __init__(self, list_proxy_file_path) -> None:
        self._list_proxy_file_path = list_proxy_file_path
        with open(list_proxy_file_path) as f:
            proxy_list_raw_str = f.read()
        super().__init__(proxy_list_raw_str)

if __name__ == '__main__' :
    pp1 = FileListProxyProvider('util/proxy/proxy_list.txt')
    print(pp1)
    for i in range(0, pp1.proxies_count):
        if not pp1.check_proxy():
            pp1.block_proxy()
        else:
            pp1.rotate_proxy()
    print(pp1)
    pass