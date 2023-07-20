import os
import shutil
import logging
from util.parser import Parser
from .podcast_site import PodcastSite

class PodcastParser(Parser):

    def __init__(self, driver, log_file = 'podcast_parser.log', output_dir = os.path.curdir, common_dir = True, clear_dir = True, exit_if_not_found = True, episode_first = 1, episode_last = None) -> None:
        super().__init__(driver, log_file)
        if common_dir : # if common folder for saving files
            self._mp3_output_dir = output_dir
            self._pdf_output_dir = output_dir
            if os.path.exists(output_dir) and clear_dir:
                shutil.rmtree(output_dir)     
        else:
            self._mp3_output_dir = os.path.join(output_dir, 'mp3')
            self._pdf_output_dir = os.path.join(output_dir, 'pdf')
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