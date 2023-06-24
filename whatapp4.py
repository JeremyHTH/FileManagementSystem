import random
import string
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from GenerateMessage import Generate_Message
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service

BASE_URL = "https://web.whatsapp.com/"
CHAT_URL = "https://web.whatsapp.com/send?phone={phone}&text&type=phone_number&app_absent=1"

def ReadData(path: str):
    import pandas
    try: 
        df = pandas.read_excel(path)
        print(df)
    except Exception as e:
        print(e)

    
def SendMessage():
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    user_data_dir = ''.join(random.choices(string.ascii_letters, k=8))
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-data/" + user_data_dir)
    chrome_options.add_argument("--incognito")

    browser = webdriver.Chrome(ChromeDriverManager().install(),  options=chrome_options,)

    # browser = webdriver.Chrome(service=Service(r"C:\Chrome_driver\chromedriver"),  options=chrome_options,)

    browser.get(BASE_URL)
    browser.maximize_window()

    Data = Generate_Message()

    if (input('Break point : ') != ""):
        return
        

    for Phone, Message in Data:

        browser.get(CHAT_URL.format(phone=Phone))
        time.sleep(3)


        inp_xpath = (
            '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
        )
        input_box = WebDriverWait(browser, 60).until(
            expected_conditions.presence_of_element_located((By.XPATH, inp_xpath))
        )
        # input_box.send_keys(Message)

        for Line in Message:
            input_box.send_keys(Line)
            ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).perform()
            ActionChains(browser).key_up(Keys.SHIFT).perform()
        
        input_box.send_keys(Keys.ENTER)

        time.sleep(2)

    

if __name__ == '__main__':
    SendMessage()

# https://pythoncircle.com/post/775/automating-whatsapp-web-using-selenium-to-send-messages/

# https://www.google.com/search?q=auto+login+whatsapp+web+with+selenium&oq=auto+login+whatsapp+web+with+selenium&aqs=edge..69i57j0i546l3.2039j0j1&sourceid=chrome&ie=UTF-8      