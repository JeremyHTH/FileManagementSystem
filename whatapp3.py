from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def main():
    driver = webdriver.Chrome(executable_path=r'C:\\ChromeDriver\\chromedriver_win32\\chromedriver')
    driver.get('https://web.whatsapp.com/')

    input('Press enter after scanning QR code and logging in')

    if (input('Break point : ') != ""):
        return
    search_box = driver.find_element_by_xpath('//div[@contenteditable="true"][@data-tab="3"]')
    search_box.send_keys('Free drive')
    search_box.send_keys(Keys.ENTER)

    if (input('Break point : ') != ""):
        return
    
    input_box = driver.find_element_by_xpath('//div[@contenteditable="true"][@data-tab="6"]')
    input_box.send_keys('Your message goes here')
    input_box.send_keys(Keys.ENTER)

    time.sleep(5) # wait for message to be sent

    driver.quit()

if __name__ == '__main__':
    main()
