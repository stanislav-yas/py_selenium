import os
import logging
from util.parser import Parser
from .podcast_site import PodcastSite

class PodcastParser(Parser):

    def __init__(self, driver, log_file = 'podcast_parser.log', output_dir = os.path.curdir, common_dir = True, episode_first = 1, episode_last = None) -> None:
        super().__init__(driver, log_file)
        if common_dir :
            self._mp3_output_dir = output_dir
            self._pdf_output_dir = output_dir              
        else:
            self._mp3_output_dir = os.path.join(output_dir, 'mp3')
            self._pdf_output_dir = os.path.join(output_dir, 'pdf')
        #TODO Check output_dir availability   
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
                episode.download_mp3(self._mp3_output_dir)
                episode.download_pdf(self._pdf_output_dir)
                logging.info(f'Episode #{episode.number_str} - "{episode.title}" saved')
                self.parsed_episodes_count += 1
                episode_number += 1
        logging.info(f'Tolal {self.parsed_episodes_count} episodes saved')

if __name__ == '__main__':
    from selenium import webdriver
    PodcastParser(driver = webdriver.Firefox()).start()