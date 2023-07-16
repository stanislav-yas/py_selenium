from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def scrollIntoViewJS(driver: WebDriver, element: WebElement):
  driver.execute_script("arguments[0].scrollIntoView(false);",element)
