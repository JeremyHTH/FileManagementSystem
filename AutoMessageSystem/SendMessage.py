from io import TextIOBase
import random
import string
import time
import sys, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import *

from AutoMessageSystem.GenerateMessage import GenerateStudentMessage
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service

from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtCore import Qt

BASE_URL = "https://web.whatsapp.com/"
CHAT_URL = "https://web.whatsapp.com/send?phone={phone}&text&type=phone_number&app_absent=1"

def SendMessage(Data, LogFile: TextIOBase):

    LogFile.write(f'{time.ctime()[4:]}\tStart send message\n')

    FailedNumber = []

    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    user_data_dir = ''.join(random.choices(string.ascii_letters, k=8))
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-data/" + user_data_dir)
    chrome_options.add_argument("--incognito")

    try:
        browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()),  options=chrome_options,)
    except:
        browser = webdriver.Chrome(service=Service(r"C:\ChromeDriver\chrome-win32\chromedriver"),  options=chrome_options,)

    try:
        browser.get(BASE_URL)
        browser.maximize_window()
    except:
        LogFile.write(f'{time.ctime()[4:]}\tFailed to open browser\n')
        QMessageBox.warning(None,"Send message", "Failed to open browser", QMessageBox.Ok)
        return

    # Data, NotFoundName = GenerateStudentMessage(MessageFilePath, ContactFilePath)
    buttonReply = QMessageBox.question(None, 'Automation System', 'Press Yes if you have logged in to Whatsapp.', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel) #.setWindowFlags(QMessageBox().windowFlags() | Qt.WindowStaysOnTopHint)
    if (not buttonReply == QMessageBox.Yes):
        QMessageBox.information(None,"Send Message","Cancelled",QMessageBox.Ok)
        LogFile.write(f'{time.ctime()[4:]}\tLog in failed\n')
        try:
            browser.close()
        except:
            pass
        return 
    

    for Phone, Message in Data:

        try:
            browser.get(CHAT_URL.format(phone=Phone))
            time.sleep(3)


            inp_xpath = (
                '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
            )
            input_box = WebDriverWait(browser, 30).until(
                expected_conditions.presence_of_element_located((By.XPATH, inp_xpath))
            )
            # input_box.send_keys(Message)

            for Line in Message:
                input_box.send_keys(Line)
                ActionChains(browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).perform()
                ActionChains(browser).key_up(Keys.SHIFT).perform()
            
            input_box.send_keys(Keys.ENTER)

            time.sleep(2)

            LogFile.write(f'{time.ctime()[4:]} {Phone} Send Success.\n')
        # except WebDriverException as e:
        #     LogFile.write(f'{time.ctime()[3:]} {Phone} Send failed.\n{str(e)}')
        #     FailedNumber.append(Phone)

        except Exception as e:
            LogFile.write(f'{time.ctime()[4:]} {Phone} Send failed.\n{str(e)}')
            FailedNumber.append(Phone)
    try:
        browser.close()
    except Exception as e:
        pass

    return FailedNumber

if __name__ == '__main__':
    app = QApplication(sys.argv)
    SendMessage()

# https://pythoncircle.com/post/775/automating-whatsapp-web-using-selenium-to-send-messages/

# https://www.google.com/search?q=auto+login+whatsapp+web+with+selenium&oq=auto+login+whatsapp+web+with+selenium&aqs=edge..69i57j0i546l3.2039j0j1&sourceid=chrome&ie=UTF-8      