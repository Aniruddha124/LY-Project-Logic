import numpy as np
import pandas as pd
import pickle
import json
import time
import os
from datetime import datetime
from query import get_address_details
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def addToCSV(row, df, filepath):
    hdr = False if os.path.isfile(filepath) else True
    df_temp = df
    df_temp = df_temp.append(row, ignore_index=True)
    df_temp.to_csv(filepath, index=False, mode="a", header=hdr)


def addTransactionInfo(tx, transactionFilepath, dfTransactions):
    hash = tx["transaction"]["hash"]
    sender = tx["sender"]["address"]
    receiver = tx["receiver"]["address"]
    amount = tx["amount"]
    timestamp = str(tx["transaction_more_info"][0]["timestamp"])

    new_row = {
        "hash": hash,
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "timestamp": timestamp
    }
    addToCSV(new_row, dfTransactions, transactionFilepath)


def Generator(addresses, filename, offset):
    df = pd.DataFrame(
        columns=[
            "address",
            "in_btc",  # Total BTC received or Inbound Amount
            "out_btc",  # Total BTC sent or Outbound Amount
            "balance",
            "in_degree",  # Total number of inbound transactions
            "out_degree",  # Total number of outbound transactions
            "unique_in_degree",
            "unique_out_degree",
            "mean_in_btc",  # Average number of inbound transactions per address
            "mean_out_btc",  # Average number of outbound transactions per address
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
            "in_amount_frequency",  # In Velocity
            "out_amount_frequency",  # Out Velocity
        ]
    )

    errDf = pd.DataFrame(
        columns=["address"])

    dfTransactions = pd.DataFrame(
        columns=[
            "hash",
            "sender",
            "receiver",
            "amount",
            "timestamp",
        ]
    )

    filepath = './Datasets_Generated/AddressInfo/' + str(filename) + '.csv'
    transactionFilepath = './Datasets_Generated/TransactionInfo/' + \
        "transaction_" + str(filename) + '.csv'
    errFilepath = './Datasets_Generated/SkippedAddressInfo/' + \
        str(filename) + '_skipped.csv'

    for count, address in enumerate(addresses):

        print(f"Scanning {count+offset}) {address}")
        # if (count+offset == 101):
        #     break
        try:
            address_details = get_address_details(address)

            in_btc = address_details['data']['bitcoin']['address_stats'][0]['address']['inflows']
            out_btc = address_details['data']['bitcoin']['address_stats'][0]['address']['outflows']
            balance = address_details['data']['bitcoin']['address_stats'][0]['address']['balance']

            in_degree = address_details['data']['bitcoin']['address_stats'][0]['address']['inboundTransactions']
            out_degree = address_details['data']['bitcoin']['address_stats'][0]['address']['outboundTransactions']

            unique_in_degree = address_details['data']['bitcoin']['address_stats'][0]['address']['uniqueSenders']
            unique_out_degree = address_details['data']['bitcoin']['address_stats'][0]['address']['uniqueReceivers']

            mean_in_btc = (in_btc / in_degree) if (in_degree > 0) else 0
            mean_out_btc = (out_btc / out_degree) if (out_degree > 0) else 0

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

            active_days_count = max((datetime.strptime(last_active, "%Y-%m-%dT%H:%M:%S%fZ") -
                                     datetime.strptime(first_active, "%Y-%m-%dT%H:%M:%S%fZ")).days, 1)
            in_transaction_frequency = in_degree / active_days_count

            out_transaction_frequency = out_degree / active_days_count

            in_amount_frequency = in_btc / active_days_count
            out_amount_frequency = out_btc / active_days_count

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

            addToCSV(new_row, df, filepath)
            print(
                f"{bcolors.OKGREEN}  [\u2713]  Address Info added {bcolors.ENDC}")

            # incoming transaction info
            for tx in address_details['data']['bitcoin']['incoming_transactions']:
                addTransactionInfo(tx, transactionFilepath, dfTransactions)

            # outgoing transaction info
            for tx in address_details['data']['bitcoin']['outgoing_transactions']:
                addTransactionInfo(tx, transactionFilepath, dfTransactions)

            print(
                f"{bcolors.OKGREEN}  [\u2713]  Transaction Info added {bcolors.ENDC}")

        except Exception as e:
            print(f"{bcolors.FAIL}{bcolors.BOLD}Error! {e}{bcolors.ENDC}")

            new_row = {"address": address}
            addToCSV(new_row, errDf, errFilepath)
            print(
                f"{bcolors.WARNING}  [\u2713]  Skipped Info added {bcolors.ENDC}")

            continue

    # df.to_csv('./Datasets_Generated/' + str(filename) +
    #           '.csv', index=False, header=True)


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

# addresses = ["bc1qwukmzzjqn5hwsp4uaswc4c53gc0xz5asrv0prx","bc1qgdjqv0av3q56jvd82tkdjpy7gdp9ut8tlqmgrpmv24sq90ecnvqqjwvw97"]
# Generator(addresses,"Output")


if __name__ == '__main__':
    dataframe = pd.read_csv('./Scraper/cleaned_dataset/heist_addresses.csv')
    addresses = dataframe['# address'].tolist()
    split_data = list(split(addresses, 10))

    section = 0  # Change this to the section you want to generate
    offset = 0  # chnage this to start from the nth row of the chosen section

    print(
        f"{bcolors.UNDERLINE}{bcolors.OKGREEN}Processing Section {section} for {len(split_data[section])} Addresses from {offset}th row {bcolors.ENDC}")

    Generator(split_data[section][offset:], "Output_" + str(section), offset)
