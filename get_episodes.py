from selenium import webdriver
import os
from speakenglishpodcast_com.podcast_parser import PodcastParser
import logging

# logging = logging.getLogger("get_episode")
# logging.basicConfig(
#     filename='get_episodes.log',
#     filemode='w',
#     encoding='utf-8',
#     format='%(asctime)s|%(levelname)s|%(module)s|%(message)s',
#     datefmt='%d/%m/%Y %H:%M:%S',
#     level=logging.INFO, 
#     )
# logging.debug('debug message')
# logging.info('info message')
# logging.warning('warn message')
# logging.error('error message')
# logging.critical('critical message')

print('Script started')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
# prefs = {
#     # "download.default_directory": "./output"
#     }
# options.add_experimental_option("prefs",prefs)
log_file = os.path.join('speakenglishpodcast_com', 'podcast_parser.log')
parser = PodcastParser(driver=webdriver.Chrome(options=options), 
              log_file=log_file, 
              output_dir='output', 
              common_dir=False,
              exit_if_not_found=False, 
              clear_dir=True, 
              episode_first=198, 
              episode_last=200,
              )
parser.start()
print('Script finished')