from requests import options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def gog_info(game_name:str):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(),options=options))
    query = game_name.replace(" ", "+")
    url = f"https://www.gog.com/en/games?query={query}&order=desc:score"
    driver.get(url)
    time.sleep(3) 
    try:
        title = driver.find_element(By.XPATH,"//product-title[@selenium-id='productTitle']/span").text
        price = driver.find_element(By.XPATH,"//price-value[@selenium-id='productPriceValue']/span").text.replace("$", "").strip()       
        price = float(price)*85.84
        return{
            "source": "gog",
            "title": title,
            "price": price
        }
    except Exception as e:
        print(f"Error occured: {e}")
        return None
    finally:
        driver.quit()

def buy_gog(title):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(),options=options))
    title = title.replace(" ", "_").replace(":", "")
    url = f"https://www.gog.com/en/game/{title}"
    print(url)
    driver.get(url)
    time.sleep(5)
    try:
        buy_button = driver.find_element(By.CLASS_NAME, "buy-now-button")
        buy_button.click()
        print("Successfully purchased on GOG")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
            driver.quit()