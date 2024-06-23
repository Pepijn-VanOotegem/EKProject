#!/usr/bin/env python3

import os
import csv
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium_stealth import stealth

#variabelen
csv_file_path = './data/csv/scrappen/wedstrijdenFlashScore.csv'

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
    huidige_jaar = datetime.datetime.now().year
    return [jaar for jaar in range(1960, huidige_jaar + 1, 4)]

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    edities = get_jaren()

    for jaar in edities:
        try: 
            response = driver.get(f"https://www.flashscore.nl/voetbal/europa/ek-{jaar}/uitslagen/")
            time.sleep(0.5)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            homeTeams = soup.find_all('div', class_='_participant_x6lwl_4 event__homeParticipant')

            namesHomeTeams = []
            for team in homeTeams:
                team_span = team.find('span', class_='_simpleText_zfz11_4 _webTypeSimpleText01_zfz11_8 _name_x6lwl_17')
                if team_span:
                    namesHomeTeams.append(team_span.get_text())
                
                team_strong = team.find('strong', class_='_simpleText_zfz11_4 _webTypeSimpleText01_zfz11_8 _bold_zfz11_57 _name_x6lwl_17')
                if team_strong:
                    namesHomeTeams.append(team_strong.get_text())
            
            awayTeams = soup.find_all('div', class_='_participant_x6lwl_4 event__awayParticipant')

            namesAwayTeams = []
            for team in awayTeams:
                team_span = team.find('span', class_='_simpleText_zfz11_4 _webTypeSimpleText01_zfz11_8 _name_x6lwl_17')
                if team_span:
                    namesAwayTeams.append(team_span.get_text())
                
                team_strong = team.find('strong', class_='_simpleText_zfz11_4 _webTypeSimpleText01_zfz11_8 _bold_zfz11_57 _name_x6lwl_17')
                if team_strong:
                    namesAwayTeams.append(team_strong.get_text())
            
            ScoresHome = soup.find_all('div', class_='event__score event__score--home')

            scoreHome = []
            for score in ScoresHome:
                score = score.get_text()
                scoreHome.append(score)
            
            ScoresAway = soup.find_all('div', class_='event__score event__score--away')

            scoreAway = []
            for score in ScoresAway:
                score = score.get_text()
                scoreAway.append(score)

            tijdstippen = soup.find_all('div', class_='event__time')
            tijdsgegevens = []

            for tijdstip in tijdstippen:
                tijdstip = tijdstip.get_text()[:12]
                tijdsgegevens.append(tijdstip)


            for i in range(len(namesHomeTeams)):
                csv_writer.writerow([jaar, tijdsgegevens[i], namesHomeTeams[i], namesAwayTeams[i], scoreHome[i], scoreAway[i]]) 

        except UnexpectedAlertPresentException:
                    alert = Alert(driver)
                    alert.accept()  # of alert.dismiss()
                    print(f"Alert gesloten voor jaar {jaar}. Overslaan naar volgend jaar.")
                    continue

print(f"Data is succesvol geschreven naar {csv_file_path}")

driver.quit()

