from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from util.parser import Parser
from util.proxy.list_proxy_provider import ListProxyProvider


pp1 = ListProxyProvider(proxy_list_file='util/proxy/ru_proxy_list.txt')
parser = Parser(browser_headless=False, proxy_provider=pp1)
driver = parser.driver
driver.get('https://api.myip.com/')
body = driver.find_element(by=By.TAG_NAME, value='body')
body.text
# parser.rotate_driver(delay=1)
# driver.get('https://api.myip.com/')
# body = driver.find_element(by=By.TAG_NAME, value='body')
driver.quit()