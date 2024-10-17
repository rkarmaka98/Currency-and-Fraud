import pandas as pd
import requests

# Replace 'YOUR_APP_ID' with your actual Open Exchange Rates API key
API_KEY = '46632c01d8904cd6ab2e4dc8c239ab40'
BASE_URL = 'https://openexchangerates.org/api'

# Function to fetch exchange rates from the Open Exchange Rates API
def get_latest_exchange_rates():
    url = f'{BASE_URL}/latest.json?app_id={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('rates', {})
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return {}

# Function to process the data and calculate the total amount in USD
def process_data(subtask1_df, exchange_rates):
    total_usd_value = 0.0
    
    # Iterate over the rows in the dataframe
    for _, row in subtask1_df.iterrows():
        amount = row['amount']
        currency = row['currency']
        
        # Check if the currency is available in the exchange rates
        if currency in exchange_rates:
            conversion_rate = exchange_rates[currency]

            # Calculate the USD equivalent of the amount
            usd_value = amount/conversion_rate
            total_usd_value += usd_value
        else:
            print(f"Currency {currency} not found in exchange rates. Skipping.")
    
    return total_usd_value

def main():
    # Load the CSV file for subtask1
    subtask1_df = pd.read_csv('subtask1/subtask1.csv')  # Contains 'amount', 'currency'
    
    # Fetch the latest exchange rates
    exchange_rates = get_latest_exchange_rates()
    
    if exchange_rates:
        # Process the data and calculate the total value in USD
        total_usd_value = process_data(subtask1_df, exchange_rates)
        
        # Print the total value in USD
        print(f"Total value in USD: {total_usd_value:.2f}")
    else:
        print("Failed to fetch exchange rates.")

if __name__ == '__main__':
    main()
