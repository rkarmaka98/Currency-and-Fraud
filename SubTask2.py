import requests
import pandas as pd

# Replace 'YOUR_APP_ID' with your actual Open Exchange Rates API key
API_KEY = '46632c01d8904cd6ab2e4dc8c239ab40'
BASE_URL = 'https://openexchangerates.org/api'

def get_latest_exchange_rates():
    url = f'{BASE_URL}/latest.json?app_id={API_KEY}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('rates', {})
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return {}

def process_data(subtask1_df, subtask2_df, exchange_rates):
    total_usd_value = 0.0
    
    # Merge subtask1 and subtask2 on the currency column to apply the fees to the corresponding amounts
    merged_data = pd.merge(subtask1_df, subtask2_df, on='currency', how='left')
    
    # Iterate over the rows in the merged dataframe
    for _, row in merged_data.iterrows():
        amount = row['amount']
        currency = row['currency']
        fee = row['fee'] * 100
        
        # Check if the currency is in the exchange rates dictionary
        if currency in exchange_rates:
            conversion_rate = exchange_rates[currency]

            # Apply the rules based on the fee
            if fee > 8.0:
                # Skip processing the amount
                print(f"Skipping {amount} {currency} due to high fee ({fee}%).")
                continue
            elif fee < 3.0:
                # Double the amount
                amount *= 2
                print(f"Doubling the amount for {currency} due to low fee ({fee}%).")

            # Calculate the USD equivalent of the amount
            amount = (amount * fee) / 100
            usd_value = amount / conversion_rate
            total_usd_value += usd_value
        else:
            print(f"Currency {currency} not found in exchange rates. Skipping.")
    
    return total_usd_value

def main():
    # Load the CSV files for subtask1 and subtask2
    subtask1_df = pd.read_csv('subtask1.csv')  # Contains 'amount', 'currency'
    subtask2_df = pd.read_csv('subtask2.csv')  # Contains 'fee', 'currency'
    
    # Fetch the latest exchange rates
    exchange_rates = get_latest_exchange_rates()
    
    if exchange_rates:
        # Process the data based on the rules
        total_usd_value = process_data(subtask1_df, subtask2_df, exchange_rates)
        
        # Print the total value in USD
        print(f"Total value in USD: {total_usd_value:.2f}")
    else:
        print("Failed to fetch exchange rates.")

if __name__ == '__main__':
    main()
