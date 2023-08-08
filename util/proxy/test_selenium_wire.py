from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import json
from list_proxy_provider import ListProxyProvider
import time

# https://github.com/qwj/python-proxy - another proxy
# mitmdump --set mode=upstream:https://de873.nordvpn.com:89 --set upstream_auth=<user>:<pass>

options = webdriver.ChromeOptions()
# Configure any desired options for the Chrome browser
options.add_argument('--headless')
pp = ListProxyProvider('util/proxy/proxy_list.txt')
proxy = pp.proxies[0]
seleniumwire_options = {
    'verify_ssl': False  # Verify SSL certificates but beware of errors with self-signed certificates    
    # 'proxy': {
    #     'https': f'{proxy[0]}://{proxy[3]}:{proxy[4]}@{proxy[1]}:{proxy[2]}',
    }
 
# Create a WebDriver instance with Selenium Wire
driver = webdriver.Chrome(seleniumwire_options=seleniumwire_options, options=options)

# Define a request interceptor function
def my_request_interceptor(request):
    # Do something with the intercepted request
    print(f"Intercepted request: {request.url}")
    # Block image assets
    if request.path.endswith(('.png', '.jpg', '.gif')):
        request.abort()    
 
# Define a response interceptor function
def my_response_interceptor(request, response):
    # Do something with the intercepted response
    print(f"Intercepted response: {response.status_code}")
 
# Set the request interceptor
# driver.request_interceptor = my_request_interceptor
 
# Set the response interceptor
# driver.response_interceptor = my_response_interceptor
 
# Make request
def check_ip(driver):
    driver.get('https://httpbin.org/ip')
    el = driver.find_element(By.CSS_SELECTOR, 'body')
    result = json.loads(el.text)
    return result['origin']

pp = ListProxyProvider('util/proxy/proxy_list.txt')
for i in range(0, pp.proxies_count-2):
    proxy = pp.proxies[i]
    driver.proxy = {
            # 'http': f'http://{proxy_url}',
            # 'https': f'https://{proxy_url}',
            # 'http': f'socks5://{proxy_url}',
            # 'https': f'socks5://{proxy_url}',
            'http': f'{proxy[0]}://{proxy[3]}:{proxy[4]}@{proxy[1]}:{proxy[2]}',
            'https': f'{proxy[0]}://{proxy[3]}:{proxy[4]}@{proxy[1]}:{proxy[2]}',
            'no_proxy': 'localhost, 127.0.0.1',
        }
    print(driver.backend.master.server.config.upstream_server) #debug
    if i != 0:
        wait = 40
        print(f'Waiting {wait}sec...')
        time.sleep(wait)
    print(f'proxy: {proxy[1]} - origin: {check_ip(driver)}')
# driver.requests[1].response.headers.get('Content-Type')
pass
# Close the driver
driver.quit()

