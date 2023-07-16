from selenium import webdriver
from speakenglishpodcast_com.get_episodes_parser import GetEpisodesParser


options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "./output"}
options.add_experimental_option("prefs",prefs)
GetEpisodesParser(driver=webdriver.Chrome(options=options)).start()
