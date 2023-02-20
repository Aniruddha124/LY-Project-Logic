import numpy as np
import pandas as pd
import pickle
import json
import time
from TXDetails import get_complete_tx_details

def Generator(starter_hashes, timeout, filename):
    scanned_addresses = []
    df = pd.DataFrame(columns=["address", "score"])
    
    for address in starter_hashes:
        new_row = {'address': address, 'score': 100}
        df = df.append(new_row, ignore_index=True)

    # Initial DataFrame with only Malicious Addresses
    # print(df)

    start_time = time.time()
    timeout_time = start_time + timeout

    for address in starter_hashes:
        # print(time.time())

        if  time.time() > timeout_time:
            break

        if address not in scanned_addresses:
            print(f"Scanning {address}")
            scanned_addresses.append(address)
            tx_data = get_complete_tx_details(address)
            # print(tx_data['data'])
            # in_degree = len(tx_data['data']['bitcoin']['inbound'])
            # out_degree = len(tx_data['data']['bitcoin']['outbound'])
            current_score = df.loc[df['address'] == address, 'score'].iloc[0]
            print(f"Current score: {current_score}")
            # Process inbound transactions
            in_txs = tx_data['data']['bitcoin']['inbound']
            for tx in in_txs:
                print(f"Sender {tx['sender']['address']}")
                if (tx['sender']['address'] in df['address'].unique()):
                    score = df.loc[df['address'] == tx['sender']['address'], 'score'].iloc[0]
                    new_score = (score + current_score) / 2
                    df.loc[df['address'] == tx['sender']['address'], 'score'] = new_score
                    print(f"Updated Score for {tx['sender']['address']} with Score: {new_score}")
                else:
                    new_row = {'address': tx['sender']['address'], 'score': (current_score + 0)/2}
                    df = df.append(new_row, ignore_index=True)
                    print(f"Added {tx['sender']['address']} with Score: {(current_score + 0)/2}")
            starter_hashes.insert(len(starter_hashes)+1, tx['sender']['address'] )
        else:
            continue
    
    # Final DataFrame with all Addresses        
    print(df)    
    df.to_csv('./Generated/' + str(filename) + '.csv', index=False)



starter_addresses = ["bc1qwukmzzjqn5hwsp4uaswc4c53gc0xz5asrv0prx"]

Generator(starter_addresses, 10, "Output")



