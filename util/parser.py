import os
import logging
from selenium import webdriver
import time

class Parser:

    def __init__(self, driver, output_dir = os.path.curdir, log_file = 'parser.log', log_level = logging.DEBUG, screenshot_on_error = True) -> None:
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
        # logging.basicConfig(
        #   filename=log_file,
        #   filemode='w',
        #   encoding='utf-8',
        #   format='%(asctime)s|%(levelname)s|%(module)s|%(message)s',
        #   datefmt='%d/%m/%Y %H:%M:%S',
        #   level=logging.INFO, 
        #   )
        self._log_file = log_file
        self._log_level = log_level
        self._output_dir = output_dir
        self._screenshot_on_error = screenshot_on_error
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
          if self._screenshot_on_error:
            self.driver.get_screenshot_as_file(os.path.join(self._output_dir,"screenshot_error.png"))
        try:
          self.finalize()
        except Exception as err:
          logging.error(f'Error occured in parser.finalize(): {err}')
          if self._screenshot_on_error:
            self.driver.get_screenshot_as_file(os.path.join(self._output_dir,"screenshot_error.png"))

    def finalize(self) -> None:
        if self.driver != None:
          self.driver.quit()
