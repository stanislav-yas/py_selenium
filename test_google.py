from selenium import webdriver
driver = webdriver.Chrome()
driver.get("http://www.google.com")
elem = driver.find_element(by="name", value="q")
elem.send_keys("Hello WebDriver!")
elem.submit()
print(driver.title)
driver.quit()