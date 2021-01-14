import requests
import json
import csv
import time
from bs4 import BeautifulSoup
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def number_req(number):
    return int(number[0]) < 5

def title_req(title):
    title = title.lower()
    for item in ["capstone", "senior", "research", "project"]:
        if item in title:
            return True
    return False

def credit_req(areas, skills):
    return "WR" in skills or "Hu" in areas or "So" in areas

def get_email(driver, names):
    data = []
    for name in names:
        url = f"https://directory.yale.edu/?queryType=term&pattern={name}&title=professor"
        driver.get(url)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        res = soup.select('a[href^=mailto]')

        if len(res) != 1:
            print(name, res)
        
        if not res:
            data.append("?")
            continue

        res = res[0]

        if not res.text or res.text == "Email":
            data.append("?")
        else:
            data.append(res.text)
    return ", ".join(data)

url = "https://old.coursetable.com/gen/json/data_202101.json"
req = requests.get(url)
data = json.loads(req.text)

chrome_options = Options()
chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(options = chrome_options)

with open("results.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Course Code", "Course Name", "Professor Name", "Professor Email"])
    for item in data:
        if len(item["professors"]) > 0 and number_req(item["number"]) and (title_req(item["long_title"]) or credit_req(item["areas"], item["skills"])):
            code = item["subject"] + " " + item["number"]
            writer.writerow([code, item["long_title"], ", ".join(item["professors"]), get_email(driver, item["professors"])])
