import os
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
        self.mp3_href = parser.driver.find_element(by='css selector', value=_mp3_sel).get_attribute('href')
        self.pdf_href = parser.driver.find_element(by='css selector', value=_pdf_sel).get_attribute('href')

    def download_mp3(self, dir_name: str):
        file_name = f'episode#{episode_num_to_str(self.number)}.mp3'
        mp3_file_path = os.path.join(dir_name, file_name)
        if self.mp3_href != None:
            return request.urlretrieve(self.mp3_href, mp3_file_path)

    def download_pdf(self, dir_name: str):
        file_name = f'episode#{episode_num_to_str(self.number)}.pdf'
        pdf_file_path = os.path.join(dir_name, file_name)
        if self.pdf_href != None:
            return request.urlretrieve(self.pdf_href, pdf_file_path)

def episode_num_to_str(num: int) -> str:
    num_str = str(num)
    if num < 10:
        num_str = '00' + num_str
    elif num < 100:
        num_str = '0' + num_str
    return num_str