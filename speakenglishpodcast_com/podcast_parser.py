import os
import shutil
import logging
import time
from typing import Type
from selenium import webdriver
from util.parser import Parser
from .podcast_site import PodcastSite
from util.proxy.proxy_provider import ProxyProvider

class PodcastParser(Parser):

    def __init__( self,
                 driver: webdriver.Chrome | webdriver.Firefox | None = None,
                 driver_type: Type[webdriver.Chrome] | Type[webdriver.Firefox] = webdriver.Chrome,
                 browser_headless = True,
                 proxy_provider: ProxyProvider | None = None,
                 output_dir = os.path.curdir,
                 log_file = 'podcast_parser.log',
                 log_level = logging.INFO,
                 common_dir = True,
                 clear_dir = True,
                 exit_if_not_found = True,
                 episode_first = 1,
                 episode_last = None
                 ) -> None:
        super().__init__( driver = driver,
                         driver_type = driver_type,
                         browser_headless = browser_headless,
                         proxy_provider = proxy_provider,
                         output_dir = output_dir,
                         log_file = log_file,
                         log_level = log_level
                        )
        if common_dir : # if common folder for saving files
            self._mp3_output_dir = self._output_dir
            self._pdf_output_dir = self._output_dir
            if os.path.exists(self._output_dir) and clear_dir:
                shutil.rmtree(self._output_dir)     
        else:
            self._mp3_output_dir = os.path.join(self._output_dir, 'mp3')
            self._pdf_output_dir = os.path.join(self._output_dir, 'pdf')
            if os.path.exists(self._mp3_output_dir) and clear_dir:
                shutil.rmtree(self._mp3_output_dir) #deleting folder if 'clear_dir' set
            if os.path.exists(self._pdf_output_dir) and clear_dir:
                shutil.rmtree(self._pdf_output_dir)                  
        #creating output_dir if not exists
        if not os.path.exists(self._mp3_output_dir):
            os.makedirs(self._mp3_output_dir)
        if not common_dir and not os.path.exists(self._pdf_output_dir):
            os.makedirs(self._pdf_output_dir)

        self._episode_first = episode_first
        self._episode_last = episode_last
        self._exit_if_not_found = exit_if_not_found
        self.parsed_episodes_count = 0
        logging.debug('PodcastParser initialized')
    
    def run(self) -> None:
        # driver.set_window_rect(x=1920, y=0, width=1900, height=1000)
        site = PodcastSite(self)
        episode_number = self._episode_first
        while self._episode_last == None or (self._episode_last != None and episode_number <= self._episode_last):
            episode = site.search_episode(episode_number)
            if episode == None:
                st = f'Episode #{episode_number} not found'
                if  self._exit_if_not_found or self._episode_last == None:
                    logging.warning(f"{st} - exiting...")
                    break
                logging.warning(st)
                time.sleep(3) #timeout 3s after previous not successful search
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