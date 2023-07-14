from selenium import webdriver

class Parser:

    def __init__(self, driver = None) -> None:
        if driver == None:
            driver = webdriver.Chrome()
        self.driver = driver
    
    def run(self) -> None:
        '''The main parsing flow - should be implemented in derived class - '''
        raise NotImplementedError("You should implement the main parsing flow in method 'run()'")
    
    def start(self) -> None:
        self.run()
        self.finalize()

    def finalize(self) -> None:
        if self.driver != None:
          self.driver.quit()
