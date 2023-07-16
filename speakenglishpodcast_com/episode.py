from util.parser import Parser
from util.util import scrollIntoViewJS
from urllib import request

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

    def download_mp3(self):
        scrollIntoViewJS(self._parser.driver, self.pdf_el)
        self.mp3_el.click()

    def download_pdf(self):
        request.urlretrieve(self.pdf_el.get_attribute('href'), f'./output/episode{self.number}.pdf')
        # self._parser.driver.execute_script("var el = $('h2 + ul li:nth-child(2) > a'); el[0].setAttribute     ('download','225'); el[0].scrollIntoView(false); el[0].click()",self.pdf_el)