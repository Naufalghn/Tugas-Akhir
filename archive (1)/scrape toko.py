from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

#url = input("Masukkan url toko : ")
url = "https://www.tokopedia.com/rikisparepart-1/review"

if url :
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    data = []
    next=True
    while next:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.findAll('article', attrs = {'class':'css-ccpe8t'})

        for container in containers:
            try:
                review = container.find('span', attrs = {'data-testid':'lblItemUlasan'}).text
                data.append(
                    (review)
                )
            except AttributeError:
                continue

        time.sleep(2)
        try:
            element = driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']")
            if element.get_property('disabled'):
                next=False
            else:
                next=True
            element.click()
            print("tombol next ada")
           
        except NoSuchElementException:
            print("tombol next tidak ada")
            next=False

        #driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']").click()
        time.sleep(3)


    print(data)
    df = pd.DataFrame(data, columns=["Ulasan"])
    df.to_csv("TAScrape.csv", index=False)