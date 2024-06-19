#!/usr/bin/env python3

import os
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth

#variabelen
csv_file_path = './data/csv/scrappen/wedstrijdenSite2.csv'

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

if not os.path.exists('data/csv/scrappen/'):
    os.makedirs('data/csv/scrappen/')

def get_jaren():
    response = driver.get("https://www.fcupdate.nl/voetbalcompetities/internationaal/europees-kampioenschap/programma-uitslagen/2020")
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    select_tag = soup.find('select', id='season-search')
    options = select_tag.find_all('option')
    jaren = []

    for option in options:
        jaar = option.get_text(strip=True)
        jaren.append(jaar)

    return jaren

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    Edities = get_jaren()

    for jaar in Edities:
        response = driver.get(f"https://www.fcupdate.nl/voetbalcompetities/internationaal/europees-kampioenschap/programma-uitslagen/{jaar}")
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        rijen = soup.find_all('div', class_='matches-panel')

        datum = ''
        for rij in rijen:
            klasse = rij.get('class')

            if 'notes' in klasse:
                datum = rij.get_text()
            elif 'Played' in klasse:
                thuisploeg = rij.find('a', class_='left-team')
                thuisploeg = thuisploeg.find('span').get_text()

                uitploeg = rij.find('a', class_='right-team')
                uitploeg = uitploeg.find('span').get_text()

                score = rij.find('div', class_='match-result').get_text()
                score = score.split('-')
                scoreThuis = score[0]
                scoreUit = score[1]
            
                csv_writer.writerow([str(datum).strip(), 'EK', 'groepfase', thuisploeg, uitploeg, int(scoreThuis), int(scoreUit)]) 

print(f"Data is succesvol geschreven naar {csv_file_path}")

driver.quit()

