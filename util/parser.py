from datetime import datetime
import os
import logging
from typing import Type
from selenium import webdriver
from selenium.webdriver.common.by import By
from util.proxy.list_proxy_provider import ListProxyProvider

class Parser:

    def __init__( self, 
                  driver: webdriver.Chrome | webdriver.Firefox | None = None,
                  driver_type: Type[webdriver.Chrome] | Type[webdriver.Firefox] = webdriver.Chrome,
                  browser_headless = True,
                  proxy_provider: ListProxyProvider | None = None,
                  output_dir = os.path.curdir, 
                  log_file = 'parser.log', 
                  log_level = logging.DEBUG, 
                  screenshot_on_error = True
                ) -> None:
        self._driver_type = driver_type
        self._browser_headless = browser_headless
        self._pp = proxy_provider
        self._log_file = log_file
        self._log_level = log_level
        self._output_dir = output_dir
        self._screenshot_on_error = screenshot_on_error        
         # create file handler
        fh = logging.FileHandler(
           filename= log_file,
           mode='w',
           encoding='utf-8',
           )
        # create console handler
        ch = logging.StreamHandler()
        logging.basicConfig(
           format='%(asctime)s|%(levelname)s|%(module)s|%(message)s',
           datefmt='%d/%m/%Y %H:%M:%S',
           level=log_level,
           handlers=[fh, ch]
        )
        if driver is None:
           self.init_driver()
        else:
           self.driver = driver

    def init_driver(self):
        if issubclass(self._driver_type, webdriver.Chrome):
            options = webdriver.ChromeOptions()
            if self._browser_headless == True:
                options.add_argument('--headless')
            if self._pp is not None:
               proxy = self._pp.proxy
               if proxy is not None:
                options.add_argument(f"--proxy-server=127.0.0.1:{proxy.lport}")
            self.driver=webdriver.Chrome(options=options)
        elif issubclass(self._driver_type, webdriver.Firefox):
            options = webdriver.FirefoxOptions()
            if self._browser_headless:
                options.add_argument('-headless')
            self.driver=webdriver.Firefox(options=options)
        else:
            raise Exception(f'Unsupported driver type: {self._driver_type}')
        
    def rotate_driver(self, random_change: bool = False, delay: int = 0):
        """Rotate driver. 
            - If not 'random_change', then switches to the next available proxy, 
            - delay in seconds (float)
        """        
        if self.driver is not None:
           self.driver.quit()
        if self._pp is not None:
           self._pp.rotate_proxy(random_change=random_change, delay=delay)
        self.init_driver()
    
    def run(self) -> None:
        '''The main parsing flow - should be implemented in derived class - '''
        raise NotImplementedError("You should implement the main parsing flow in method 'run()'")
    
    def start(self) -> None:
        try:
          self.started = datetime.now()
          logging.info('Parser started')        
          self.run()
          self.finished = datetime.now()
          logging.info(f'Parser finished. Elapsed time = {self.finished - self.started}')            
        except Exception as err:
          logging.error(f'Error occured in parser.run(): {err}')
          if self._screenshot_on_error and self.driver is not None:
            self.driver.get_screenshot_as_file(os.path.join(self._output_dir,"screenshot_error.png"))
        try:
          self.finalize()
        except Exception as err:
          logging.error(f'Error occured in parser.finalize(): {err}')
          if self._screenshot_on_error and self.driver is not None:
            self.driver.get_screenshot_as_file(os.path.join(self._output_dir,"screenshot_error.png"))

    def finalize(self) -> None:
        if self.driver is not None:
          self.driver.quit()

if __name__ == '__main__' :
    pp1 = ListProxyProvider(proxy_list_file='util/proxy/ru_proxy_list.txt')
    parser = Parser(browser_headless=False, proxy_provider=pp1)
    driver = parser.driver
    driver.get('https://api.myip.com/')
    body = driver.find_element(by=By.TAG_NAME, value='body')
    parser.rotate_driver(delay=1)
    driver.get('https://api.myip.com/')
    body = driver.find_element(by=By.TAG_NAME, value='body')