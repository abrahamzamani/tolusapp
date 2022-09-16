from   selenium import webdriver
from   selenium.webdriver.common.by import By
# from   selenium.webdriver.common.keys import Keys
from   selenium.common.exceptions import NoSuchElementException
from   selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from   selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import  os


class Paraphraser:
    def __init__(self):
        self.firefox_driver_path = "driver/geckodriver"
        self.service = Service (executable_path=self.firefox_driver_path)
        self.options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(options=self.options, service=self.service)
#--------------------------------------------------------------------------------------------
        self.log_in()
    
    def log_in(self):
        self.driver.get ('https://quillbot.com/login?returnUrl=/')
        self.driver.implicitly_wait(60)

        #................................LOGIN TO QUILBOT SECTION START...............................................#
        # self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div/header/div/div[3]/div/button[3]').click()
        # self.driver.find_element(By.CSS_SELECTOR, "button[title='Log In']").click()
        self.driver.find_elements(By.CLASS_NAME, "css-t94qzu")[0].send_keys("x10act@gmail.com")
        self.driver.find_elements(By.CLASS_NAME, "css-t94qzu")[1].send_keys("zealoT19")
        self.driver.find_element(By.CLASS_NAME, "css-jbqyw4").click()
        #................................LOGIN TO QUILBOT SECTION END...............................................#

    def paraphrased_data(self, data):
        self.driver.implicitly_wait(10)
        #................................ENTER DATA TO BE PARAPHRASED START..........................................#
        send_text = self.driver.find_element (By.ID, "inputText")
        send_text.send_keys (data)
        paraphrase_button = self.driver.find_element (By.CSS_SELECTOR, ".quillArticleBtn")
        paraphrase_button.click ()
        #................................ENTER DATA TO BE PARAPHRASED END..........................................#

        try:
            self.driver.find_element(By.XPATH, '//*[@id="max-width-dialog-title"]/button').click()

        except NoSuchElementException:
            pass

        #...............................GET PARAPHRASED DATA.START.......................................................#
        
        get_paraphrased_text = self.driver.find_element (By.ID, "editable-content-within-article")
        rawHtml = get_paraphrased_text.get_attribute ('innerHTML')
        text = BeautifulSoup(rawHtml, features='html.parser').text
        # print(text)
        #...................CLICK THE POP UP BOX TO CONFIRM DELETING TEXT IF IT APPEAR END...............................#
        


        try:
            # time.sleep (5)
            delete_btn = self.driver.find_element(By.XPATH, '//*[@id="modeControlsStickyContainer-default"]/div/div[3]/div/button')
            delete_btn.click ()
        except:
            time.sleep(2)
            print("2 seconds")
            delete_btn = self.driver.find_element(By.XPATH, '//*[@id="modeControlsStickyContainer-default"]/div/div[3]/div/button')
            delete_btn.click ()

        time.sleep(1)
        try:
            # checkbox = self.driver.find_element(By.CLASS_NAME, "css-1m9pwf3").click()
            continue_btn = self.driver.find_element(By.XPATH,'//button[normalize-space()="CONTINUE"]').click()
        except NoSuchElementException:
            continue_btn = self.driver.find_element(By.XPATH,'//button[normalize-space()="CONTINUE"]').click()

        return text

    def log_out(self):
        self.driver.find_element(By.CLASS_NAME, "BaseBadge-root").click()
        self.driver.find_element(By.CLASS_NAME, "BaseBadge-root").click()
        print("done2")
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//*[text()='Log Out']").click()
        
       