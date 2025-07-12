from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def steam_info(game_name:str):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(),options=options))
    query = game_name.replace(" ", "+")
    url = f"https://store.steampowered.com/search/?term={query}&supportedlang=english&ndl=1"
    driver.get(url)
    time.sleep(3) 
    try:
        title = driver.find_element(By.CLASS_NAME, "title").text
        price = driver.find_element(By.CLASS_NAME, "discount_final_price").text.replace("₹", "").strip()
        return{
            "source": "steam",
            "title": title,
            "price": price
        }
    except Exception as e:
        print(f"Error occured: {e}")
        return None
    finally:
        driver.quit()
    

def buy_steam(title):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    title = title.replace(" ", "_")
    url = f"https://store.steampowered.com/search/?term={title}&supportedlang=english&ndl=1"
    driver.get(url)
    time.sleep(3)
    try:
        buy_button = driver.find_element(By.CLASS_NAME, "search_result_row")
        buy_button.click()
        time.sleep(5)
        cart_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn_addtocart"))
        )
        add_to_cart_button = cart_div.find_element(By.TAG_NAME, "a")
        add_to_cart_button.click()
        print("Successfully purchased on Steam")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()
    return