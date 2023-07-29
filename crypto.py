import os
import csv
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding="utf-8")

CHROME_DRIVER_PATH = "chromedriver"
BASE_URL = "https://www.coingecko.com"

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get("https://www.coingecko.com/fr/all-cryptocurrencies")
time.sleep(5)

# Create a directory to store the scraped files
directory = "Athena/AnalyseScrapp/scraped_data"
if not os.path.exists(directory):
    os.makedirs(directory)

# Retrieve the HTML content of the table
html_content = driver.page_source
soup = BeautifulSoup(html_content, "html.parser")
table = soup.find("table", class_="table")

# Get the first 30 rows from the table
rows = table.select("tbody tr")[:30]

counter = 1

for row in rows:
    # Extract the URL from the first cell of the row
    url = row.find("a")["href"]
    coin_name = row.find("a").find("span").text

    # Convert the relative URL to a complete URL
    full_url = urljoin(BASE_URL, url)

    # Open the URL in a new driver instance
    driver_row = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    driver_row.get(full_url)
    time.sleep(5)
    a_elements = driver_row.find_elements(By.TAG_NAME, "a")
    iCoin = [i.text for i in a_elements].index("Données historiques")
    print(iCoin)
    a_elements[iCoin].click()
    time.sleep(5)
    a_elements = driver_row.find_elements(By.TAG_NAME, "span")
    iCoin = [i.text for i in a_elements].index("1y")
    a_elements[iCoin].click()
    time.sleep(5)
    for i in range(6) : 
        a_elements = driver_row.find_elements(By.TAG_NAME, "button")
        iCoin = [i.text for i in a_elements].index("En savoir plus")
        a_elements[iCoin].click()
        time.sleep(2)
    # Retrieve the HTML content of the historical data table
    html_content_row = driver_row.page_source
    soup_row = BeautifulSoup(html_content_row, "html.parser")
    table_row = soup_row.find("table", class_="table")

    # Extract the data and write to a CSV file
    name = os.path.join(directory, f"{coin_name}.csv")
    with open(name, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Check if the file is empty
        is_file_empty = csvfile.tell() == 0

        if is_file_empty:
            # Write the headers of the table if it's the first row
            header_texts = [th.text.strip() for th in table_row.select("thead th")]
            writer.writerow(header_texts)

        # Write the rows of the table
        rows_row = table_row.select("tbody tr")
        for row_row in rows_row:
            row_texts = [td.text.strip() for td in row_row.select("th, td")]
            writer.writerow(row_texts)

    driver_row.quit()
    counter += 1

driver.quit()


import os
import csv
import pandas as pd
import numpy as np

directory = "Athena/AnalyseScrapp/scraped_data"
cleaned_directory = "Athena/AnalyseScrapp/clean"

# Vérifier si le dossier "clean" existe, sinon le créer
if not os.path.exists(cleaned_directory):
    os.makedirs(cleaned_directory)

# Parcourir tous les fichiers CSV dans le dossier "crypto"
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        input_file = os.path.join(directory, filename)
        output_file = os.path.join(cleaned_directory, filename)

        # Ouvrir le fichier CSV en mode lecture
        with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        # Supprimer les espaces et le symbole dollar des colonnes "Cours d'ouverture" et "Cours de fermeture"
        for row in rows[1:]:  # Ignorer l'en-tête
            row[3] = float(row[3].replace(' ', '').replace('$', '').replace(',', '.'))
            if row[4] != 'N/A':
                try:
                    row[4] = float(row[4].replace(' ', '').replace('$', '').replace(',', '.'))
                except ValueError:
                    row[4] = np.nan  # Replace invalid value with NaN

        # Convertir la colonne "Volume" en float
        df = pd.DataFrame(rows[1:], columns=rows[0])  # Convertir les données en DataFrame
        try:
            df['Volume'] = df['Volume'].str.replace('$', '').str.replace(' ', '').str.replace(',', '.').astype(float)
        except ValueError:
            df['Volume'] = np.nan  # Replace invalid value with NaN

        # Enregistrer les modifications dans un nouveau fichier CSV dans le dossier "clean"
        df.to_csv(output_file, index=False)
