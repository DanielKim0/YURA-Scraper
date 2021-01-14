from selenium import webdriver
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def shadow(driver, element):
    # Works in Chrome only!
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root

class CourseTableParser:
    def __init__(self):
        self.driver = webdriver.Chrome()
        load_dotenv()

    def signin(self):
        self.driver.get("https://old.coursetable.com/Table")
        username = self.driver.find_element_by_name("username")
        username.send_keys(os.environ.get("USERNAME"))
        password = self.driver.find_element_by_name("password")
        password.send_keys(os.environ.get("PASSWORD"))
        self.driver.find_element_by_name("submit").click()
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        self.driver.find_elements_by_tag_name("button")[0].click()

        wait = WebDriverWait(self.driver, 60)
        wait.until(lambda driver: driver.current_url == "https://old.coursetable.com/Table")

    def extract(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "tbody"))
        )
        source = self.driver.page_source
        self.driver.close()
        return source

    def parse(self, source):
        soup = BeautifulSoup(source, "html.parser")
        table = soup.find("table")
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) # Get rid of empty values
        print(data)

    def main(self):
        self.signin()
        source = self.extract()
        self.parse(source)

if __name__ == "__main__":
    p = CourseTableParser()
    p.main()