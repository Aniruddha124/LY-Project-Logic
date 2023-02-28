import numpy as np
import pandas as pd
import pickle
import json
import time
from datetime import datetime
from WalletDetails import get_wallet_details
from TXDetails import get_complete_tx_details

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
            "first_in_tx_timestamp",
            "first_out_tx_timestamp",
            "last_in_tx_timestamp",
            "last_out_tx_timestamp",
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
            address_details = get_wallet_details(address)
            address_data = get_complete_tx_details(address)
            
            in_btc = address_details['data']['bitcoin']['inputs'][0]["value"]
            out_btc = address_details['data']['bitcoin']['outputs'][0]["value"]
            balance = abs(out_btc - in_btc)

            in_degree = len(address_data['data']['bitcoin']['inbound'])
            out_degree = len(address_data['data']['bitcoin']['outbound'])

            in_address_list = []
            for tx in address_data['data']['bitcoin']['inbound']:
                in_address_list.append(tx['sender']['address'])
            unique_in_degree = len(set(in_address_list))
            # print(f"Unique Inbound Addresses: {unique_in_degree}")

            out_address_list = []
            for tx in address_data['data']['bitcoin']['outbound']:
                out_address_list.append(tx['receiver']['address'])
            unique_out_degree = len(set(out_address_list))
            # print(f"Unique Outbound Addresses: {unique_out_degree}")


            mean_in_btc = in_btc / in_degree
            mean_out_btc = out_btc / out_degree

            first_in_tx_timestamp = address_details['data']['bitcoin']['inputs'][0]["min_date"]
            last_in_tx_timestamp = address_details['data']['bitcoin']['inputs'][0]["max_date"]
            first_out_tx_timestamp = address_details['data']['bitcoin']['outputs'][0]["min_date"]
            last_out_tx_timestamp = address_details['data']['bitcoin']['outputs'][0]["max_date"]


            in_tx_values = []
            for tx in address_data['data']['bitcoin']['inbound']:
                in_tx_values.append(tx['amount'])

            max_in_btc = max(in_tx_values)
            min_in_btc = min(in_tx_values)

            out_tx_values = []
            for tx in address_data['data']['bitcoin']['outbound']:
                out_tx_values.append(tx['amount'])
                
            max_out_btc = max(out_tx_values)
            min_out_btc = min(out_tx_values)

            in_standard_deviation = np.std(in_tx_values)
            out_standard_deviation = np.std(out_tx_values)

            in_transaction_frequency = in_degree/(datetime.strptime(last_in_tx_timestamp, "%Y-%m-%d") - datetime.strptime(first_in_tx_timestamp, "%Y-%m-%d")).days
            out_transaction_frequency = out_degree/(datetime.strptime(last_out_tx_timestamp, "%Y-%m-%d") - datetime.strptime(first_out_tx_timestamp, "%Y-%m-%d")).days
            # print(f"Inbound Transaction Frequency: {in_transaction_frequency}")
            # print(f"Outbound Transaction Frequency: {out_transaction_frequency}")
            
            in_amount_frequency = in_btc/(datetime.strptime(last_in_tx_timestamp, "%Y-%m-%d") - datetime.strptime(first_in_tx_timestamp, "%Y-%m-%d")).days
            out_amount_frequency = out_btc/(datetime.strptime(last_out_tx_timestamp, "%Y-%m-%d") - datetime.strptime(first_out_tx_timestamp, "%Y-%m-%d")).days

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
                "first_in_tx_timestamp": first_in_tx_timestamp,
                "first_out_tx_timestamp": first_out_tx_timestamp,
                "last_in_tx_timestamp": last_in_tx_timestamp,
                "last_out_tx_timestamp": last_out_tx_timestamp,
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

dataframe = pd.read_csv('./Scraper/cleaned_dataset/heist_addresses.csv')
addresses = dataframe['# address'].tolist()
split_data = list(split(addresses, 50))
print(len(split_data[0]))

Generator(split_data[0],"Output_0")