from selenium import webdriver
import os
from speakenglishpodcast_com.podcast_parser import PodcastParser

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# prefs = {
#     # "download.default_directory": "./output"
#     }
# options.add_experimental_option("prefs",prefs)
log_file = os.path.join('speakenglishpodcast_com', 'podcast_parser.log')
parser = PodcastParser(
            # browser_headless=False,
            # driver_type=webdriver.Firefox,
            log_file=log_file,
            output_dir='output',
            common_dir=True,
            exit_if_not_found=False,
            clear_dir=True,
            episode_first=199,
            episode_last=201,
            )
parser.start()