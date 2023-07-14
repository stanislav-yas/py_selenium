from util.parser import Parser
from .podcast_site import PodcastSite

class GetEpisodesParser(Parser):
    
    def run(self) -> None:
        driver = self.driver
        driver.set_window_rect(x=1920, y=0, width=1900, height=1000)
        # driver.get("http://www.google.com")
        # elem = driver.find_element(by=By.NAME, value="q")
        # elem.send_keys("Hello WebDriver!")
        # elem.submit()
        # print(driver.title)
        site = PodcastSite(self)
        episode = site.search_episode(235)
        if episode != None:
            print(episode.get_mp3())
            print(episode.get_pdf())
        pass

if __name__ == '__main__':
    from selenium import webdriver
    GetEpisodesParser(driver = webdriver.Firefox()).start()