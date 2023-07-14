from util.parser import Parser

class Episode:
    
    def __init__(self, parser: Parser, href: str) -> None:
        self.href = href
        self.parser = parser
        parser.driver.get(href)
    
    def get_mp3(self) -> str:
        a= self.parser.driver.find_elements(by='css selector', value='h2 + ul li:nth-child(1) > a')
        if len(a) > 0:
            href = a[0].get_attribute('href')
            return href
        else:
            return ""
        
    def get_pdf(self) -> str:
        a= self.parser.driver.find_elements(by='css selector', value='h2 + ul li:nth-child(2) > a')
        if len(a) > 0:
            href = a[0].get_attribute('href')
            return href
        else:
            return ""        