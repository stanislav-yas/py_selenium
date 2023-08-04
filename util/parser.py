from datetime import datetime
import os
import logging
from typing import Type
from selenium import webdriver
from util.proxy.proxy_provider import ProxyProvider

class Parser:

    def __init__( self, 
                  driver: webdriver.Chrome | webdriver.Firefox | None = None,
                  driver_type: Type[webdriver.Chrome] | Type[webdriver.Firefox] = webdriver.Chrome,
                  browser_headless = True,
                  proxy_provider: ProxyProvider | None = None,
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
        if driver == None:
           self.init_driver()
        else:
           self.driver = driver

    def init_driver(self):
        if issubclass(self._driver_type, webdriver.Chrome):
            options = webdriver.ChromeOptions()
            if self._browser_headless == True:
                options.add_argument('--headless')
            self.driver=webdriver.Chrome(options=options)
        elif issubclass(self._driver_type, webdriver.Firefox):
            options = webdriver.FirefoxOptions()
            if self._browser_headless:
                options.add_argument('-headless')
            self.driver=webdriver.Firefox(options=options)
        else:
            raise Exception(f'Unsupported driver type: {self._driver_type}') 
    
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
          if self._screenshot_on_error and self.driver != None:
            self.driver.get_screenshot_as_file(os.path.join(self._output_dir,"screenshot_error.png"))
        try:
          self.finalize()
        except Exception as err:
          logging.error(f'Error occured in parser.finalize(): {err}')
          if self._screenshot_on_error and self.driver != None:
            self.driver.get_screenshot_as_file(os.path.join(self._output_dir,"screenshot_error.png"))

    def finalize(self) -> None:
        if self.driver != None:
          self.driver.quit()
