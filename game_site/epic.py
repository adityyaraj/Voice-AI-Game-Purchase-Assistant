from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def epic_info(game_name:str):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(),options=options))
    query = game_name.replace(" ", "%20")
    url = f"https://store.epicgames.com/en-US/browse?q={query}&sortBy=relevancy&sortDir=DESC&count=40"
    driver.get(url)
    time.sleep(3) 
    try:
        title = driver.find_element(By.CLASS_NAME, "css-rgqwpc").text
        price = driver.find_element(By.XPATH, "//span[contains(text(), '$')]").text
        return{
            "source": "epic",
            "title": title,
            "price": price
        }
    except Exception as e:
        print(f"Error occured: {e}")
        return None

def buy_epic(title):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(),options=options))
    query = title.replace(" ", "%20")
    url = f"https://store.epicgames.com/en-US/p/{query}"
    driver.get(url)
    time.sleep(3)
    try:
        buy_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Buy')]")
        buy_button.click()
        print("Successfully purchased on Epic Games")
    except Exception as e:
        print(f"Error occurred: {e}")
    driver.quit()
    return