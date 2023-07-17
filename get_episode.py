from selenium import webdriver
import logging
from speakenglishpodcast_com.get_episodes_parser import GetEpisodesParser

# logging = logging.getLogger("get_episode")
logging.basicConfig(
    filename='get_episode.log', 
    encoding='utf-8',
    format='%(asctime)s|%(levelname)s|%(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    # level=logging.WARNING, 
    )
logging.debug('debug message')
logging.info('info message')
logging.warning('warn message')
logging.error('error message')
logging.critical('critical message')
# logging.info('Program started')
# options = webdriver.ChromeOptions()
# prefs = {
#     # "download.default_directory": "./output"
#     }
# options.add_experimental_option("prefs",prefs)
# GetEpisodesParser(driver=webdriver.Chrome(options=options)).start()
# logging.info('Program stopped')