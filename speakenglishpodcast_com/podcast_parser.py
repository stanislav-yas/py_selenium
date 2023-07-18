import os
import logging
from util.parser import Parser
from .podcast_site import PodcastSite

class PodcastParser(Parser):

    def __init__(self, driver, log_file = 'podcast_parser.log', output_dir = os.path.curdir, episode_first = 1, episode_last = None) -> None:
        super().__init__(driver, log_file)
        self._output_dir = output_dir
        self._episode_first = episode_first
        self._episode_last = episode_last
        self.parsed_episodes_count = 0
    
    def run(self) -> None:
        # driver.set_window_rect(x=1920, y=0, width=1900, height=1000)
        site = PodcastSite(self)
        episode_number = self._episode_first
        while self._episode_last == None or (self._episode_last != None and episode_number <= self._episode_last):
            episode = site.search_episode(episode_number)
            if episode == None:
                logging.warning(f'Episode #{episode_number} not found - exiting...')
                break
            else:
                self.parsed_episodes_count += 1
                result = episode.download_mp3(self._output_dir)
                result = episode.download_pdf(self._output_dir)
                logging.info(f'Episode #{episode.number_str} - "{episode.title}" saved')
                episode_number += 1
        logging.info(f'Tolal {self.parsed_episodes_count} episodes saved')

if __name__ == '__main__':
    from selenium import webdriver
    PodcastParser(driver = webdriver.Firefox()).start()