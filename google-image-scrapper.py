from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import requests
import keyboard
import os


def download_img_by_url(url, path):
    """Downloads the image and saves it in the given directory"""
    response = requests.get(url, timeout=10)  # Set timeout for image download
    if response.status_code == 200:
        image_content = response.content

        with open(path, "wb") as file:
            file.write(image_content)
            print("The image has been successfully downloaded!")
    else:
        print("An error occurred while downloading!")


def scroll_website():
    """Scrolls to the bottom of the website"""
    while True:
        browser.execute_script("window.scrollBy(0, 300);")

        if keyboard.is_pressed("s"):
            break

        try:
            browser.find_element(By.CLASS_NAME, "LZ4I").click()
            sleep(3)
        except:
            pass


SEARCH_PHRASE = "dogs"  # Your search phrase
DRIVER_PATH = r"""C:/Users/wilko/Desktop/Studia/Projekty swoje/Python/
Machine learning/Country-leaders-face-recognition/msedgedriver.exe"""  # Path to your chromium driver

service = Service(DRIVER_PATH)
options = Options()
browser = webdriver.Edge(service=service, options=options)
wait = WebDriverWait(
    driver=browser, timeout=2
)  # timeout >= 10 for lower download speeds
browser.maximize_window()
browser.get("https://www.google.com/imghp?hl=EN")

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
os.makedirs(
    f"C:/Users/wilko/Desktop/Studia/Projekty swoje/Python/Machine learning/Face-Classification-Project/images/{SEARCH_PHRASE}",
    exist_ok=True,
)

for img_id, thumbnail in enumerate(thumbnails):
    thumbnail.click()

    try:
        image = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "r48jcc.pT0Scc.iPVvYb"))
        )
        img_url = image.get_attribute("src")
        try:
            download_img_by_url(
                url=img_url,
                path=f"C:/Users/wilko/Desktop/Studia/Projekty swoje/Python/Machine learning/Face-Classification-Project/images/{SEARCH_PHRASE}/{img_id}.PNG",
            )
        except requests.Timeout:
            print("Image download timed out. Skipping to the next image...")
            continue
    except TimeoutException:
        continue

browser.quit()
