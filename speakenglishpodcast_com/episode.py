from util.parser import Parser

_title_sel = 'h1.entry-title'
_mp3_sel = 'h2 + ul li:nth-child(1) > a'
_pdf_sel = 'h2 + ul li:nth-child(2) > a'
class Episode:
    
    def __init__(self, parser: Parser, number: int, href: str) -> None:
        self.number = number
        self.href = href
        self._parser = parser
        parser.driver.get(href)
        self.title = parser.driver.find_element(by='css selector', value=_title_sel).text
        self.mp3_el = parser.driver.find_element(by='css selector', value=_mp3_sel)
        self.pdf_el = parser.driver.find_element(by='css selector', value=_pdf_sel)

    