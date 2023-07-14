from selenium import webdriver
from speakenglishpodcast_com.get_episodes_parser import GetEpisodesParser

GetEpisodesParser(driver=webdriver.Chrome()).start()
