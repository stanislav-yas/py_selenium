from selenium.webdriver.common.by import By
from .episode import Episode
from util.parser import Parser

class PodcastSite:
    def __init__(self, parser: Parser) -> None:
        self.parser = parser

    def search_episode(self, num: int)-> Episode | None:
        num_str = _normalize(num)
        s = f'https://speakenglishpodcast.com/?s=%23{num_str}'
        driver = self.parser.driver
        driver.get(s)
        a = driver.find_elements(by=By.CSS_SELECTOR, value='article .entry-title > a')
        if len(a) > 0:
            href = a[0].get_attribute('href')
            return Episode(self.parser, href)
        else:
            return None
        
def _normalize(num: int) -> str:
    num_str = str(num)
    if num < 10:
        num_str = '00' + num_str
    elif num < 100:
        num_str = '0' + num_str
    return num_str