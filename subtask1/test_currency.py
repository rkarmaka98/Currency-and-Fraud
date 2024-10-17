# test_currency_converter.py

import pandas as pd
from SubTask2 import process_data

# Simulated data for subtask1 (amount and currency) and subtask2 (fee and currency)
subtask1_data = {'amount': [400], 'currency': ['EUR']}
subtask2_data = {'fee': [0.01], 'currency': ['EUR']}  # 1% fee in decimal

# Convert to pandas DataFrame
subtask1_df = pd.DataFrame(subtask1_data)
subtask2_df = pd.DataFrame(subtask2_data)

# Simulate fetching exchange rates (mocked for testing)
def get_mocked_exchange_rates():
    return {'USD': 1.1}  # Example: 1 EUR = 1.1 USD

def test_process_data():
    # Use mocked exchange rates instead of real ones for testing
    exchange_rates = get_mocked_exchange_rates()
    
    # Process the data and calculate the total value in USD
    total_usd_value = process_data(subtask1_df, subtask2_df, exchange_rates)
    
    # Check the output
    print(f"Total value in USD: {total_usd_value:.2f}")
    
if __name__ == '__main__':
    test_process_data()
