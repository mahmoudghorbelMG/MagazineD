import schedule
import time
import os
import datetime
import pytz

def execute_crypto_code():
    os.system("python crypto.py")

def execute_scrapping_code():
    os.system("python scrapping.py")

# Créer un objet timezone pour le Royaume-Uni (BST)
timezone = pytz.timezone("Europe/London")

# Convertir l'heure spécifiée en heure du Royaume-Uni
heure_britannique_crypto = datetime.time(00, 59)
heure_britannique_crypto = timezone.localize(datetime.datetime.combine(datetime.date.today(), heure_britannique_crypto))

heure_britannique_scrapping = datetime.time(1, 0)  # Exécution toutes les heures à partir de 1:00 (heure du Royaume-Uni)
heure_britannique_scrapping = timezone.localize(datetime.datetime.combine(datetime.date.today(), heure_britannique_scrapping))

# Planifier l'exécution du code de crypto à l'heure spécifiée (heure du Royaume-Uni)
schedule.every().day.at(heure_britannique_crypto.strftime("%H:%M")).do(execute_crypto_code)

# Planifier l'exécution du code de scrapping toutes les heures (heure du Royaume-Uni)
schedule.every().hour.at(heure_britannique_scrapping.strftime("%M")).do(execute_scrapping_code)

while True:
    schedule.run_pending()
    time.sleep(1)
