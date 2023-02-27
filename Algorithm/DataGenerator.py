import numpy as np
import pandas as pd
import pickle
import json
import time
from datetime import datetime
from query import get_address_details

def Generator(addresses, filename):
    df = pd.DataFrame(
        columns=[
            "address",
            "in_btc", # Total BTC received or Inbound Amount
            "out_btc", # Total BTC sent or Outbound Amount
            "balance",
            "in_degree", # Total number of inbound transactions
            "out_degree", # Total number of outbound transactions
            "unique_in_degree",
            "unique_out_degree",
            "mean_in_btc", # Average number of inbound transactions per address
            "mean_out_btc", # Average number of outbound transactions per address
            "first_active",
            "last_active",
            "max_in_btc",
            "min_in_btc",
            "max_out_btc",
            "min_out_btc",
            "in_standard_deviation",
            "out_standard_deviation",
            "in_transaction_frequency",
            "out_transaction_frequency",
            "in_amount_frequency", # In Velocity
            "out_amount_frequency", # Out Velocity
        ]
    )

    for address in addresses:
        print(f"Scanning {address}")
        try:
            address_details = get_address_details(address)

            in_btc = address_details['data']['bitcoin']['address_stats'][0]['address']['inflows']
            out_btc = address_details['data']['bitcoin']['address_stats'][0]['address']['outflows']
            balance = address_details['data']['bitcoin']['address_stats'][0]['address']['balance']

            in_degree = address_details['data']['bitcoin']['address_stats'][0]['address']['inboundTransactions']
            out_degree = address_details['data']['bitcoin']['address_stats'][0]['address']['outboundTransactions']

            unique_in_degree = address_details['data']['bitcoin']['address_stats'][0]['address']['uniqueSenders']
            unique_out_degree = address_details['data']['bitcoin']['address_stats'][0]['address']['uniqueReceivers']

            mean_in_btc = in_btc / in_degree
            mean_out_btc = out_btc / out_degree

            first_active = address_details['data']['bitcoin']['address_stats'][0]['address']['firstActive']['iso8601']
            last_active = address_details['data']['bitcoin']['address_stats'][0]['address']['lastActive']['iso8601']

            in_tx_values = []
            for tx in address_details['data']['bitcoin']['incoming_transactions']:
                in_tx_values.append(tx['amount'])
            max_in_btc = max(in_tx_values)
            min_in_btc = min(in_tx_values)

            out_tx_values = []
            for tx in address_details['data']['bitcoin']['outgoing_transactions']:
                out_tx_values.append(tx['amount'])
            max_out_btc = max(out_tx_values)
            min_out_btc = min(out_tx_values)

            in_standard_deviation = np.std(in_tx_values)
            out_standard_deviation = np.std(out_tx_values)

            in_transaction_frequency = in_degree / (datetime.strptime(last_active, "%Y-%m-%dT%H:%M:%S%fZ") - datetime.strptime(first_active, "%Y-%m-%dT%H:%M:%S%fZ")).days
            out_transaction_frequency = out_degree / (datetime.strptime(last_active, "%Y-%m-%dT%H:%M:%S%fZ") - datetime.strptime(first_active, "%Y-%m-%dT%H:%M:%S%fZ")).days

            in_amount_frequency = in_btc / (datetime.strptime(last_active, "%Y-%m-%dT%H:%M:%S%fZ") - datetime.strptime(first_active, "%Y-%m-%dT%H:%M:%S%fZ")).days
            out_amount_frequency = out_btc / (datetime.strptime(last_active, "%Y-%m-%dT%H:%M:%S%fZ") - datetime.strptime(first_active, "%Y-%m-%dT%H:%M:%S%fZ")).days


            new_row = {
                "address": address,
                "in_btc": in_btc,
                "out_btc": out_btc,
                "balance": balance,
                "in_degree": in_degree,
                "out_degree": out_degree,
                "unique_in_degree": unique_in_degree,
                "unique_out_degree": unique_out_degree,
                "mean_in_btc": mean_in_btc,
                "mean_out_btc": mean_out_btc,
                "first_active": first_active,
                "last_active": last_active,
                "max_in_btc": max_in_btc,
                "min_in_btc": min_in_btc,
                "max_out_btc": max_out_btc,
                "min_out_btc": min_out_btc,
                "in_standard_deviation": in_standard_deviation,
                "out_standard_deviation": out_standard_deviation,
                "in_transaction_frequency": in_transaction_frequency,
                "out_transaction_frequency": out_transaction_frequency,
                "in_amount_frequency": in_amount_frequency,
                "out_amount_frequency": out_amount_frequency,
            }

            # print(new_row)

            df = df.append(new_row, ignore_index=True)
        
        except:
            print(f"Something went wrong! Skipping {address}")
            continue

    print(df)
    df.to_csv('./Datasets_Generated/' + str(filename) + '.csv', index=False)

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

# addresses = ["bc1qwukmzzjqn5hwsp4uaswc4c53gc0xz5asrv0prx","bc1qgdjqv0av3q56jvd82tkdjpy7gdp9ut8tlqmgrpmv24sq90ecnvqqjwvw97"]
# Generator(addresses,"Output")

if __name__ == '__main__':
    dataframe = pd.read_csv('./Scraper/cleaned_dataset/heist_addresses.csv')
    addresses = dataframe['# address'].tolist()
    split_data = list(split(addresses, 1000))
    
    section = 0 # Change this to the section you want to generate
    
    print(f"Processing Section {section} for {len(split_data[section])} Addresses")

    Generator(split_data[section],"Output_" + str(section))