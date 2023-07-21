import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException
from .episode import Episode, episode_num_to_str
from util.parser import Parser

class PodcastSite:
    def __init__(self, parser: Parser) -> None:
        self.parser = parser
        # self.wait = WebDriverWait(parser.driver, 10)

    def search_episode(self, num: int)-> Episode | None:
        try:
            num_str = episode_num_to_str(num)
            s = f'https://speakenglishpodcast.com/?s=%23{num_str}'
            driver = self.parser.driver
            driver.get(s)
            # <div class="et_pb_text_inner">Results for "#300"</div>
            css = '#main-content .et_pb_text_inner'
            # self.wait.until(lambda d: d.find_elements(by=By.CSS_SELECTOR, value=css))
            a = driver.find_elements(by=By.CSS_SELECTOR, value='article .entry-title > a')
            if len(a) > 0:
                href = a[0].get_attribute('href')
                if href != None:
                    return Episode(self.parser, num, href)
            else:
                driver.get_screenshot_as_file(f"shot_not_found_#{num_str}.png")
            return None
        except WebDriverException as err:
            logging.error(f'Error occured in search_episode(): {err.msg}')
            raise