import numpy as np
import pandas as pd
import pickle
import json
import os
from datetime import datetime
from query import get_address_details
import warnings

def normalise_list(row):
    nor_row = []
    for i in row:
        entry = np.log1p(i)
        nor_row.append(entry)
    return np.array(nor_row)

def Score(address):
    address_details = get_address_details(address)
    # print(address_details['data'])

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
        # "address": address,
        # "in_btc": in_btc,
        # "out_btc": out_btc,
        "balance": balance,
        # "in_degree": in_degree,
        # "out_degree": out_degree,
        "unique_in_degree": unique_in_degree,
        "unique_out_degree": unique_out_degree,
        "mean_in_btc": mean_in_btc,
        "mean_out_btc": mean_out_btc,
        # "first_active": first_active,
        # "last_active": last_active,
        "max_in_btc": max_in_btc,
        "min_in_btc": min_in_btc,
        "max_out_btc": max_out_btc,
        "min_out_btc": min_out_btc,
        "in_standard_deviation": in_standard_deviation,
        "out_standard_deviation": out_standard_deviation,
        "in_transaction_frequency": in_transaction_frequency,
        "out_transaction_frequency": out_transaction_frequency,
        "in_amount_frequency": in_amount_frequency,
        "out_amount_f{requency": out_amount_frequency,
    }

    # print(len(new_row))
    req_list = list(new_row.values())
    # print(req_list)

    nor_list = normalise_list(req_list)
    # print(nor_list)

    with open('./Models/bitcoin_malicious_address_prediction.pickle', 'rb') as f:
        model = pickle.load(f)


    model_prediction = model.predict(nor_list.reshape(1, -1))

    # print(model_prediction)
    return {
        "address": address,
        "score": int(model_prediction[0]),
    }


    

if __name__ == "__main__":
    address = "bc1qwukmzzjqn5hwsp4uaswc4c53gc0xz5asrv0prx"
    score = Score(address)
    print(score)