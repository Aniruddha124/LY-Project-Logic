import numpy as np
import pandas as pd
import pickle
from Format import format_transaction_details
from TransactionDetails import get_transaction_details

with open('./Models/dt_model', 'rb') as f:
    model = pickle.load(f)

def predict(address):
    tx_data = get_transaction_details(address)
    # print(tx_data['data'])
    df = format_transaction_details(tx_data['data'])
    # print(df)
    for i in range(len(df)):
        in_degree = df.iloc[i]["in_degree"]
        out_degree = df.iloc[i]["out_degree"]
        in_btc = df.iloc[i]["in_btc"]
        out_btc = df.iloc[i]["out_btc"]
        total_btc = df.iloc[i]["total_btc"]
        mean_in_btc = df.iloc[i]["mean_in_btc"]
        mean_out_btc = df.iloc[i]["mean_out_btc"]
        is_malicious = model.predict([[in_degree, out_degree, in_btc, out_btc, total_btc, mean_in_btc, mean_out_btc]])
        print(is_malicious)


predict("bc1qcj9ujyvrf94wu0902g2lnklzlyn5j5nrr44hwp")
