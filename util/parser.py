import logging
from selenium import webdriver
import time

class Parser:

    def __init__(self, driver, log_file = 'parser.log') -> None:
        logging.basicConfig(
          filename=log_file,
          filemode='w',
          encoding='utf-8',
          format='%(asctime)s|%(levelname)s|%(module)s|%(message)s',
          datefmt='%d/%m/%Y %H:%M:%S',
          level=logging.INFO, 
          )
        self._log_file = log_file
        if driver == None:
            driver = webdriver.Chrome()
        self.driver = driver
    
    def run(self) -> None:
        '''The main parsing flow - should be implemented in derived class - '''
        raise NotImplementedError("You should implement the main parsing flow in method 'run()'")
    
    def start(self) -> None:
        try:  
          logging.info('Parser started')
          self.run()
          logging.info('Parser finished')
        except Exception as err:
          logging.error(f'Error occured in parser.run(): {err}')
          self.driver.get_screenshot_as_file("shot_error.png")
        try:
          self.finalize()
        except Exception as err:
          logging.error(f'Error occured in parser.finalize(): {err}')
          self.driver.get_screenshot_as_file("shot_error.png")

    def finalize(self) -> None:
        if self.driver != None:
          self.driver.quit()
