from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
import base64
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import csv
import re
import io
import base64
import pandas as pd
import json
import os

# Définir la fonction de test pour vérifier l'appartenance au groupe "Subscriber"
def is_subscriber(user):
    return user.groups.filter(name="Subscriber").exists()
# Décorer la vue "product" avec le décorateur "user_passes_test"
def is_authenticated(user):
    return user.is_authenticated


def tracker_bar_view(request):
    # Set the default cryptocurrency symbol to BTCUSD
    symbol = "CRYPTOCAP:BTC"

    # Check if the user has selected a different cryptocurrency
    if "symbol" in request.GET:
        symbol = request.GET["symbol"]

    context = {
        "symbol": symbol,
    }
    return render(request, "analyses/analyses.html", context)
@user_passes_test(
    lambda u: is_subscriber(u) and is_authenticated(u), login_url="subscription"
)
def currencies(request):
    labels = []
    data = []

    with open("currency_scraper/currencies.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            labels.append(row["Name"])
            price = row["Price"].replace(",", "")  # Remove the comma from the string
            data.append(float(price))
        currencies = list(reader)
        currencies = []
    # Path to the CSV file
    csv_path = "currency_scraper/currencies.csv"

    # Read the CSV file and store data in a list of dictionaries
    currencies = []
    with open(csv_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            currencies.append(row)
    labels1 = []
    data1 = []

    with open("currency_scraper/currencies.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            labels1.append(row["Name"])
            price = row["Price"].replace(",", "")  # Remove the comma from the string
            data1.append(float(price))

    return render(
        request,
        "analyses/currencies.html",
        {
            "labels1" : labels1 , 
            "data1"  : data1  , 
            "labels": labels,
            "data": data,
            "currencies": currencies,
        },
    )

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
@user_passes_test(
    lambda u: is_subscriber(u) and is_authenticated(u), login_url="subscription"
)
def crypto_data_view(request):
    # File path of the CSV file
    filename = "scrapping/coingecko_data.csv"  # Replace with the actual path to your CSV file

    # Read the CSV file using pandas
    df = pd.read_csv(filename)

    # Get the headers and data from the DataFrame
    headers = df.columns.tolist()
    data = df.values.tolist()
    
    directory = 'AnalyseScrapp/clean'

    results = []

    # Iterate over each file in the directory
    for fchier in os.listdir(directory):
        if fchier.endswith('.csv'):
            # Read the CSV file
            filepath = os.path.join(directory, fchier)
          
        Data = pd.read_csv(filepath)
      



# Handling missing values
        Data = Data.dropna(subset=['Cours de fermeture'])

# Extract the features and target variables
        X = Data[['Volume', 'Cours d\'ouverture']]
        y = Data['Cours de fermeture']

# Split the dataset into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression model
        model = LinearRegression()

# Train the model
        model.fit(X_train, y_train)

# Make predictions for the test set
        y_pred = model.predict(X_test)

# Calculate the accuracy of the model using mean squared error
        mse = mean_squared_error(y_test, y_pred)
        accuracy = 1 - (mse / y_test.var())


# Get the last row of data
        last_row = Data.iloc[-1]

# Reshape the input for prediction
        next_24_hours_volume = model.predict([[last_row['Volume'], last_row['Cours d\'ouverture']]])
        next_24_hours_opening = model.predict([[next_24_hours_volume[0], last_row['Cours d\'ouverture']]])

# Predict the next 24 hours
        next_24_hours_closing = model.predict([[next_24_hours_volume[0], next_24_hours_opening[0]]])
        

            # Store the results in a dictionary
        result = {
                'coin': fchier[:-4],
                'volume_prediction': str(next_24_hours_volume)[1:-1],
                'opening_prediction': str(next_24_hours_opening)[1:-1],
                'closing_prediction': str(next_24_hours_closing)[1:-1] ,
            }
        results.append(result)
    # Pass the data to the template context
    context = {
        'filename': filename,
        'headers': headers,
        'data': data,
        "results"  : results , 
 
    }

    return render(request, 'analyses/crypto_data.html', context)

#=======================**********************Stocks Views******************************================================================#
@user_passes_test(
    lambda u: is_subscriber(u) and is_authenticated(u), login_url="subscription"
)
def stocks_list(request):
    currencies = []
    with open("combined_output.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            currencies.append(row)
    # Read the CSV file
    data = pd.read_csv("combined_output.csv")
    # Extract the required columns
    labels = data["Symbol"]
    market_caps = data["MarketCap"]
    stock_prices = data["StockPrice"]

    # Prepare data for Chart.js
    chart_data = {
        "labels": labels.tolist(),
        "datasets": [
            {
                "label": "Market Cap",
                "data": market_caps.tolist(),
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1,
            },
            {
                "label": "Stock Price",
                "data": stock_prices.tolist(),
                "backgroundColor": "rgba(255, 99, 132, 0.2)",
                "borderColor": "rgba(255, 99, 132, 1)",
                "borderWidth": 1,
            },
        ],
    }
    return render(
        request,
        "analyses/stocks_list.html",
        {"currencies": currencies, "chart_data": chart_data},
    )


def trending(request):


    # Define file names
    file_names = ["today_Gainers", "today_losers", "Trending"]

    # List to store the table data
    tables = []

    for file_name in file_names:
        # Read the CSV file
        csv_file_path = f"scrapping/stock_data_{file_name}.csv"  # Replace with the actual path to your CSV files
        with open(csv_file_path, "r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            data = list(reader)

        # Create a DataFrame from the CSV data
        df = pd.DataFrame(data, columns=headers)

        # Convert the DataFrame to HTML table
        tableid = f"table_{file_name}"
        table_html = df.to_html(index=False, table_id=tableid, classes="table table-striped")

        # Append the table data to the list
        tables.append({"id": tableid, "html": table_html})

    return render(request, "analyses/trending.html", {"tables": tables})

#