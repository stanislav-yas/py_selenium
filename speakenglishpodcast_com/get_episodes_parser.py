import logging
from util.parser import Parser
from .podcast_site import PodcastSite

output_path = 'output'
class GetEpisodesParser(Parser):
    
    def run(self) -> None:
        driver = self.driver
        # driver.set_window_rect(x=1920, y=0, width=1900, height=1000)
        site = PodcastSite(self)
        episode_number = 225
        episode = site.search_episode(episode_number)
        if episode != None:
            logging.info(f'Episode {episode_number} found')
            result = episode.download_pdf(output_path)
            # print(episode.pdf_el)
            # episode.download_pdf()
            pass

if __name__ == '__main__':
    from selenium import webdriver
    GetEpisodesParser(driver = webdriver.Firefox()).start()