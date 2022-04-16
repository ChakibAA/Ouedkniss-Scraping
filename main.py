from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
from selenium.webdriver.chrome.options import Options

en_tete = ['name', 'categorie', 'url', 'adresse', 'mail', 'phones']


def store(stores, writer):
    for index, store in enumerate(stores):
        phones = []
        mail = []
        name_box = store.find('div', class_='__head pt-4 px-4')
        name = name_box.h1.text
        categorie = name_box.h2.text
        link = store.find(
            'a', class_="o-store-card-full v-card--light-shadow elevation-1 v-card v-card--link v-sheet theme--light")
        href = link.get('href')

        browser_store = webdriver.Chrome(
            executable_path=r"/Users/mac/Downloads/chromedriver", options=chrome_options)

        print('Store: ', index)
        print('link: ', href)
        contact = href + '/contact'
        browser_store.get(contact)
        html_store = browser_store.page_source
        soup_store = BeautifulSoup(html_store, 'html.parser')
        try:
            contact_box = soup_store.find('div', {
                'class': 'v-list elevation-1 v-sheet theme--light rounded v-list--dense v-list--nav v-list--rounded'})
            adresse_box_store = contact_box.find(
                'div', {'class': 'v-list-item v-list-item--link theme--light'})
            adresse_store = adresse_box_store.find(
                'div', {'class': 'v-list-item__content'})
            adresse_value = adresse_store.text

            info_box_store = soup_store.find_all(
                'div', {'class': 'v-list-item theme--light'})
            for index, item in enumerate(info_box_store):
                info_store = item.find_all(
                    'a', {'class': 'v-chip v-chip--clickable v-chip--link v-chip--no-color theme--light v-size--default'})
                for item in info_store:
                    temp = item.get('href')
                    print(mail)
                    print(phones)
                    print(temp)
                    if("@" in temp):
                        mail.append(temp)
                    else:
                        phones.append(temp)

        except:
            print('error')
            adresse_value = None
            mail = None
            phones = None

        ligne = [name, categorie, href, adresse_value, mail, phones]
        print(ligne)
        print('------')
        browser_store.quit()
        writer.writerow(ligne)


url = 'https://www.ouedkniss.com/boutiques'
chrome_options = Options()
chrome_options.add_argument("headless")
browser = webdriver.Chrome(
    executable_path=r"/Users/mac/Downloads/chromedriver", options=chrome_options)

browser.get(url)

time.sleep(2)

# to click pop for cookies
report1 = browser.find_element_by_xpath(
    "//button[@class='v-btn v-btn--flat v-btn--text theme--light v-size--default primary--text']")
report1.click()

index = 0

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

SCROLL_PAUSE_TIME = 10

with open('data.csv', 'w') as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=',')
    writer.writerow(en_tete)
    while True:
        html = browser.page_source

        soup = BeautifulSoup(html, 'html.parser')
        stores = soup.find_all(
            'div', {"class": 'col-sm-6 col-md-4 col-lg-3 col-12'})

        temp_stores = stores[index::]

        store(temp_stores, writer)
        # Scroll down to bottom
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script(
            "return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        index = index + 12


browser.quit()