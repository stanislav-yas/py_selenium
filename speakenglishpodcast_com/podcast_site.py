from selenium.webdriver.common.by import By
from .episode import Episode, episode_num_to_str
from util.parser import Parser

class PodcastSite:
    def __init__(self, parser: Parser) -> None:
        self.parser = parser

    def search_episode(self, num: int)-> Episode | None:
        num_str = episode_num_to_str(num)
        s = f'https://speakenglishpodcast.com/?s=%23{num_str}'
        driver = self.parser.driver
        driver.get(s)
        a = driver.find_elements(by=By.CSS_SELECTOR, value='article .entry-title > a')
        if len(a) > 0:
            href = a[0].get_attribute('href')
            if href != None:
                return Episode(self.parser, num, href)
        return None
