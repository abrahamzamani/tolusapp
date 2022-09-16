from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import os

class PaaScraper:

    def __init__(self, keyword):
        self.keyword = keyword
        self.firefox_driver_path = "driver/geckodriver"
        self.service = Service (executable_path=self.firefox_driver_path)
        self.options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(options=self.options, service=self.service)




    def scraper(self):
        self.driver.get('https://www.google.com')
        self.driver.find_element(By.NAME,"q").send_keys(self.keyword + Keys.ENTER)
        self.driver.implicitly_wait(10)

        box = self.driver.find_elements(By.CSS_SELECTOR, ".z9gcx")
        data = []
        i = 0

        while len(data) <= 3:

            question = box[i]

            #......................EXTRACT QUESTION TEXT START..........................................#
            question_text = question.get_attribute("data-q")
            print("--------------------------------------------")
            print(question_text)
            #..........................................................................................#
            question.click()
            time.sleep(3)
            box = self.driver.find_elements(By.CSS_SELECTOR, ".z9gcx")
            question = box[i]

            #......................EXTRACT ANSWER TEXT START................................................#
            try:
                answer_text = question.find_element(By.CSS_SELECTOR, ".hgKElc").get_attribute("innerHTML")
                print(answer_text)
                answer_text = BeautifulSoup(answer_text, features='html.parser').text
                
            except NoSuchElementException:
                answer_text = 0
            #................................................................................................#


            print("--------------------------------------------")

            #...................... CREATE A DICTIONARY FROM QUESTION AND ANSWER START ...................#
            each_q_and_a = dict()
            each_q_and_a["question"] = question_text
            each_q_and_a["answer"] = answer_text
            #.........................................................................................................#


            #.....................APPENDING AND REMOVING THE DICTIONARY (each_q_and_a) TO AND FROM DATA LIST..........#
            data.append(each_q_and_a)
            i+=1
            for each_data in data:
                if each_data["answer"] == 0:
                    data.pop()
            #.........................................................................................................#
        return data

    def quit_driver(self):
        self.driver.quit()
