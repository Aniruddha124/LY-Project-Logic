import numpy as np
import pandas as pd
import json
# from TransactionDetails import *

# with open('dummy2.json') as f:
#     data = json.load(f)
# print(data)

def format_transaction_details(json):
    df = pd.DataFrame(columns=["tx_hash", "in_degree", "out_degree", "in_btc", "out_btc", "total_btc", "mean_in_btc", "mean_out_btc"])
    print(df)
    in_degree = len(json['bitcoin']['inputs'])
    out_degree = len(json['bitcoin']['outputs'])
    print(in_degree)
    print(out_degree)
    for i in range(in_degree):
        new_row = {'tx_hash': json['bitcoin']['inputs'][i]['transaction']['hash'], 'in_degree': in_degree, 'out_degree': out_degree, 'in_btc': json['bitcoin']['inputs'][i]['value'], 'out_btc': 0, 'total_btc': json['bitcoin']['inputs'][i]['value'], 'mean_in_btc': json['bitcoin']['inputs'][i]['value']/in_degree, 'mean_out_btc': 0}
        df = df.append(new_row, ignore_index=True)
    
    for i in range(out_degree):
        new_row = {'tx_hash': json['bitcoin']['outputs'][i]['transaction']['hash'], 'in_degree': in_degree, 'out_degree': out_degree, 'in_btc': 0, 'out_btc': json['bitcoin']['outputs'][i]['value'], 'total_btc': json['bitcoin']['outputs'][i]['value'], 'mean_in_btc': 0, 'mean_out_btc': json['bitcoin']['outputs'][i]['value']/out_degree}
        df = df.append(new_row, ignore_index=True)
    
    return(df)

# df = format_transaction_details(data)
# print(df)