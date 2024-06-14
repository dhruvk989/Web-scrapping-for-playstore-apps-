from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from bs4 import BeautifulSoup
import os

def read_html_and_write_excel(html_file, excel_file):
    app_name = os.path.splitext(os.path.basename(html_file))[0]
    
    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    ratings = parse_ratings(soup)

    if table:
        df = pd.read_html(str(table))[0]
        df['Rating'] = ratings  # Add the ratings column to your DataFrame
        df.to_excel(excel_file, index=False)
        print(f"Data for {app_name} written to {excel_file}")
    else:
        print(f"No table found in {html_file}")

def parse_ratings(soup):
    # Assuming each review row has a unique identifier or container
    reviews = soup.find_all("tr")  # or use a more specific identifier
    ratings = []
    for review in reviews:
        stars_full = review.find_all(class_="fa fa-star")
        stars_half = review.find_all(class_="fa fa-star-half-o")
        rating = len(stars_full) + 0.5 * len(stars_half)
        ratings.append(rating)
    return ratings
def get_data_and_parse():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get("https://reviewapp.mobi/user/login")

    def login():
        try:
            email = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            password = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            submit = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="tab-sign-in"]/form/div[3]/button'))
            )
            email.send_keys("sarthak.ronaldo@gmail.com")
            password.send_keys("encryption")
            submit.send_keys(Keys.RETURN)
            print("Logged In")
            time.sleep(2)
        except Exception as e:
            print("Login Failed: ", e)
            driver.quit()

    def find_until_date(app, undate):
        page = 1
        max_pages = 1000  # You can adjust this limit based on your needs
        while page <= max_pages:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)  # Adjust timing based on page load time
            try:
                WebDriverWait(driver, 20).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, 'loader'))
                )

                parsed_table = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="reviews_here"]/table'))
                )
                if undate in driver.page_source:
                    table_html = parsed_table.get_attribute("outerHTML")
                    filename = f"{app}.html"
                    with open(filename, "w", encoding='utf-8') as file:
                        file.write(table_html)
                    print(f"Page {page} data for {app} written to {filename}")
                    break
                else:
                    # Click next page
                    next_page_button = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.ID, 'showNextPage'))
                    )
                    next_page_button.click()
                    page += 1
            except StaleElementReferenceException:
                print("Stale element error, retrying...")
                continue
            except Exception as e:
                print("Error finding data: ", e)
                break
        else:
            print(f"Reached maximum page limit for {app}")

    def parse_app(app, app_link, undate):
        driver.get("https://reviewapp.mobi/appstore-google-play-parsing")
        try:
            enter_link = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="why"]/div/div/div[2]/input'))
            )
            enter_link.send_keys(app_link)
            launch = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="show_up"]'))
            )
            launch.send_keys(Keys.RETURN)   
            print("Going to find", app)
            find_until_date(app, undate)
        except Exception as e:
            print(f"Error parsing app {app}: ", e)

    data_to_parse = [
         ["ring", "https://play.google.com/store/apps/details?id=com.ideopay.user&hl=en_IN", "2024-05-20"],
       ["Otipy", "https://play.google.com/store/apps/details?id=com.otipy.otipy&hl=en_IN", "2024-05-20"],
        ["olyv", "https://play.google.com/store/apps/details?id=in.rebase.app&hl=en&gl=IN", "2024-05-19"],
                        ["Sunstone", "https://play.google.com/store/apps/details?id=com.sunstone.hub&hl=en_IN&gl=in", "2024-05-04"],
                 ["Kissht", "https://play.google.com/store/apps/details?id=com.fastbanking", "2024-05-19"],
            ["fancall", "https://play.google.com/store/apps/details?id=com.fancall.fancallapp&hl=en_IN", "2024-04-07"],
        ["CheQ", "https://play.google.com/store/apps/details?id=com.cheq.retail", "2024-05-19"],
        ["Rummycom", "https://play.google.com/store/apps/details?id=com.rummydotcom.indianrummycashgame&hl=en", "2024-05-19"],
         ["ANQ", "https://play.google.com/store/apps/details?id=com.anqmobileapp", "2024-04-12"],
         ["MyTeam11", "https://play.google.com/store/apps/details?id=in.myteam11.store", "2024-05-19"],
        ["Pepperfry", "https://play.google.com/store/apps/details?id=com.app.pepperfry&hl=en_IN", "2024-05-19"],
            ["Zupee", "https://play.google.com/store/apps/details?id=com.zupee.free", "2024-05-20"],
        ["ruperdree", "https://play.google.com/store/apps/details?id=com.rupeeredee.app", "2024-05-20"],
        ["Vision11", "https://play.google.com/store/apps/details?id=com.vision11", "2024-05-19"],
           ["lifestyle", "https://play.google.com/store/apps/details?id=com.applications.lifestyle&hl=en", "2024-05-19"],
        ["Stanza Living", "https://play.google.com/store/apps/details?id=com.stanzaliving.app&hl=en_IN", "2024-05-19"],
          ["Jungle rummy", "https://play.google.com/store/apps/details?id=com.jungleerummy.playcashgameonline&hl=en_IN", "2024-05-19"],
          ["zag", "https://play.google.com/store/apps/details?id=com.zaggle", "2024-04-30"],
        ["Ant Mobi", "https://play.google.com/store/apps/details?id=com.ant2o.aliceblue&hl=en", "2024-05-19"],
        ["Rummy Titans", "https://play.google.com/store/apps/details?id=com.rummytitans.playcashrummyonline.cardgame", "2024-05-05"],
         ["NNNOW", "https://play.google.com/store/apps/details?id=com.nnnow.arvind&hl=en_IN", "2024-05-07"],
         ["Rummy Passion", "https://play.google.com/store/apps/details?id=com.pg.rummypassion&hl=en_IN", "2024-05-19"],
         ["Mykinara", "https://play.google.com/store/apps/details?id=com.autonom8.kinara&hl=en_IN", "2024-04-11"]
    ]

    login()
    for app, app_link, undate in data_to_parse:
        parse_app(app, app_link, undate)
        time.sleep(20)  # Adjust based on needs

        html_file_path = f"{app}_page_1.html"
        if os.path.exists(html_file_path):
            read_html_and_write_excel(html_file_path, f"{app}.xlsx")
        
    driver.quit()

get_data_and_parse()