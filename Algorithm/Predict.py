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
    # print(len(df))
    for i in range(len(df)):
        in_degree = df["in_degree"].iloc[i]
        out_degree = df["out_degree"].iloc[i]
        in_btc = df["in_btc"].iloc[i]
        out_btc = df["out_btc"].iloc[i]
        total_btc = df["total_btc"].iloc[i]
        mean_in_btc = df["mean_in_btc"].iloc[i]
        mean_out_btc = df["mean_out_btc"].iloc[i]
        # print(in_degree, out_degree, in_btc, out_btc, total_btc, mean_in_btc, mean_out_btc)
        is_malicious = model.predict([[in_degree, out_degree, in_btc, out_btc, total_btc, mean_in_btc, mean_out_btc]])
        # print(is_malicious)
        df['is_malicious'].iloc[i] = is_malicious[0]
    return(df)


prediction = predict("bc1qcj9ujyvrf94wu0902g2lnklzlyn5j5nrr44hwp")
print(prediction)