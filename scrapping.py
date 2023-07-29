import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Créer un dossier pour les fichiers de scraping s'il n'existe pas déjà
if not os.path.exists("Athena/scrapping"):
    os.makedirs("Athena/scrapping")

urls = [
    "https://stockanalysis.com/markets/gainers/",  # today
    "https://stockanalysis.com/markets/losers/",
    "https://stockanalysis.com/trending/"
]

# Définir les noms de fichier
file_names = ["today_Gainers", "today_losers", "Trending"]

# Scrapper les données depuis chaque URL et les enregistrer dans des fichiers CSV
dataframes = []
for url, file_name in zip(urls, file_names):
    # Effectuer une requête GET vers le site web
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Trouver la table contenant les données
    table = soup.find("table")

    # Extraire les en-têtes
    headers = [header.text.strip() for header in table.find_all("th")]

    # Extraire les lignes de données
    data = []
    for row in table.find_all("tr")[1:]:
        row_data = [cell.text.strip() for cell in row.find_all("td")]
        data.append(row_data)

    # Créer un DataFrame à partir des données extraites
    df = pd.DataFrame(data, columns=headers)
    dataframes.append(df)

    # Créer un fichier CSV et écrire les données
    filename = f"Athena/scrapping/stock_data_{file_name}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"Data scraped successfully from {url} and saved in {filename}.")

# Scrapper les données des crypto-monnaies
url = "https://www.coingecko.com/fr/all-cryptocurrencies"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Trouver la table contenant les données des crypto-monnaies
table = soup.find("table", class_="table")

# Extraire les données de la table
data = []
if table:
    # Extraire la ligne d'en-tête
    header_row = table.find("thead").find_all("th")
    header = [th.text.strip() for th in header_row if th.text.strip()]
    # Supprimer la colonne "Symbol" de l'en-tête
    header = [col for col in header if col != "Symbol"]
    data.append(header)

    # Extraire les lignes de données
    body_rows = table.find("tbody").find_all("tr")
    for row in body_rows:
        cells = row.find_all("td")
        # Supprimer la cellule correspondant à la colonne "Symbol"
        row_data = [cell.text.strip() for i, cell in enumerate(cells) if i != 2]
        data.append(row_data)

    # Enregistrer les données dans un fichier CSV
    filename = "Athena/scrapping/coingecko_data.csv"
    with open(filename, "w", encoding="utf-8", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data)
        print(f"Data scraped successfully from {url} and saved in {filename}.")
