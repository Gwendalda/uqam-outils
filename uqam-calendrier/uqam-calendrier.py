from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dateparser import parse
import os
import uuid
from config import *


class EvenementCalendrier:
    def __init__(self, titre:str, type:str, local:str, heure:str, jour:str, fin_de_session:str):
        self.titre = titre.replace(" ", "_")
        self.date_debut = parse(date_string=heure.split("-")[0] + " " + jour,
                                languages=['fr'], settings={'TIMEZONE': 'America/Montreal'})
        self.date_fin = parse(date_string=heure.split("-")[1] + " " + jour,
                              languages=['fr'], settings={'TIMEZONE': 'America/Montreal'})
        self.local = local.replace(" ", "_")
        self.type = type.replace(" ", "_")
        self.fin_de_session = parse(fin_de_session,
                                    languages=['fr'], settings={'TIMEZONE': 'America/Montreal'})

    def __str__(self):
        return self.titre + " " + \
               str(self.date_debut.strftime("Le %A")) + " de " + \
               str(self.date_debut.strftime("%H:%M")) + " à " + \
               str(self.date_fin.strftime("%H:%M")) + " " + \
               self.local + " " + self.type

    def __repr__(self):
        return self.__str__()

    def __dict__(self):
        return {
            "titre": self.titre,
            "date_debut": self.date_debut.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "date_fin": self.date_fin.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "local": self.local,
            "type": self.type
        }

    def get_ics_text(self):
        return "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//uqam-outils//NONSGML v1.0//EN\nBEGIN:VEVENT\nUID:" + \
               str(uuid.uuid4()) + "\nDTSTART;TZID=America/Montreal:" + self.date_debut.strftime("%Y%m%dT%H%M%S") + \
               "\nDTEND;TZID=America/Montreal:" + self.date_fin.strftime("%Y%m%dT%H%M%S") + "\nSUMMARY:" + self.titre + \
               "\nDESCRIPTION:" + self.type + "\nLOCATION:" + self.local + \
               f"\nRRULE:FREQ=WEEKLY;UNTIL={self.fin_de_session.strftime('%Y%m%dT000000Z')}" + \
               "\nEND:VEVENT\nEND:VCALENDAR"

    def produce_ics_file(self):
        # make a file with a name based on the title of the event
        with open("uqam-calendrier" + self.titre + self.type + ".ics", "w+") as f:
            f.write(self.get_ics_text())


def combine_ics_files():
    # combine all the ics files in the current directory into one
    with open("uqam-calendrier.ics", "w+") as f:
        f.write("BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//uqam-outils//NONSGML v1.0//EN\n")
        for file in os.listdir():
            if file.endswith(".ics"):
                with open(file, "r") as file_to_read:
                    # skip the lines until the first event
                    for line in file_to_read:
                        if line == "BEGIN:VEVENT\n":
                            f.write(line)
                            break
                    # write the event
                    for line in file_to_read:
                        f.write(line)
                        if line == "END:VEVENT\n":
                            break
        f.write("END:VCALENDAR")


def get_evenements(codePermanent, motDePasse):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.portailetudiant.uqam.ca/")
    username = driver.find_element(By.NAME, "codePermanent")
    passwrd = driver.find_element(By.NAME, "password")
    username.send_keys(codePermanent)
    passwrd.send_keys(motDePasse)
    driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[@type='submit']"))
    time.sleep(TIME_MULTIPLIER*1)
    driver.get("https://www.portailetudiant.uqam.ca/calendrier")
    time.sleep(TIME_MULTIPLIER*1)
    listeEvenements = []
    listeJours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    jour = 0
    for element in driver.find_elements(By.XPATH, "//div[@class='fc-event-container']"):
        for cours in element.find_elements(By.TAG_NAME, "a"):
            driver.execute_script("arguments[0].click();", cours)
            time.sleep(TIME_MULTIPLIER*0.2)
            fin_de_session = driver.find_element(By.XPATH,
                                "/html/body/div/div/div[2]/div[2]/div[2]/div[2]/div/div[2]/table/tbody/tr[4]/td/div[1]/div[1]/table/tbody/tr[3]/td[2]/p[1]").text.split("au")[1].strip()
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[text()='Retour au calendrier']"))
            time.sleep(TIME_MULTIPLIER*0.2)
            listeEvenements.append(EvenementCalendrier(cours.find_element(By.CLASS_NAME, "fc-title").text, cours.find_element(By.CLASS_NAME, "coursType").text, cours.find_element(By.CLASS_NAME, "coursLocal").text, cours.find_element(By.CLASS_NAME, "customTime").text, listeJours[jour], fin_de_session))
        jour += 1
    driver.close()
    return listeEvenements


def main():
    codePermanent = input("Code permanent: ")
    motDePasse = input("Mot de passe: ")
    listeEvenements = get_evenements(codePermanent, motDePasse)
    for evenement in listeEvenements:
        evenement.produce_ics_file()
    combine_ics_files()
    # remove all ics files except the combined one
    for file in os.listdir():
        if file.endswith(".ics") and file != "uqam-calendrier.ics":
            os.remove(file)


if __name__ == "__main__":
    main()

