from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import requests

def download_img_by_url(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        image_content = response.content

        with open(path, "wb") as file:
            file.write(image_content)
            print("Obrazek został pomyślnie pobrany")
    else:
        print("Wystąpił błąd podczas pobierania obrazka.")

def scroll_website():
    ''' Scrolls to the bottom of website '''
    last_height = browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
 
    while True:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(3)
        new_height = browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
 
        try:
            browser.find_element_by_css_selector(".YstHxe input").click()
            sleep(3)
 
        except:
            pass
 
        if new_height == last_height:
            break

        last_height = new_height

SEARCH_PHRASE = "Ana De Armas"
DRIVER_PATH = r"C:/Users/wilko/Desktop/Studia/Projekty swoje/Python/Machine learning/Country-leaders-face-recognition/msedgedriver.exe"

edge_service = Service(DRIVER_PATH)
edge_options = Options()
browser = webdriver.Edge(service=edge_service, options=edge_options)
wait = WebDriverWait(browser, 10)
browser.maximize_window()
browser.get("https://images.google.com/")

dismiss_btn = browser.find_element(By.ID, "W0wltc")
dismiss_btn.click()

sleep(1)

search_box = browser.find_element(By.NAME, "q")
search_box.send_keys(SEARCH_PHRASE)
search_btn = browser.find_element(By.CLASS_NAME, "Tg7LZd")
search_btn.click()

sleep(2)
scroll_website()

thumbnails = browser.find_elements(By.CLASS_NAME, "rg_i.Q4LuWd")

img_id = 0
for thumbnail in thumbnails:
    thumbnail.click()

    try:
        image = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "r48jcc.pT0Scc.iPVvYb")))
        img_url = image.get_attribute("src")
        download_img_by_url(url=img_url, path=f'./Data/Test/{img_id}.PNG')
    except TimeoutException:
        continue

    img_id += 1

browser.quit()