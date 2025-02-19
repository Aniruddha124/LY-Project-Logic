import numpy as np
import pandas as pd
import csv
import requests

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

def seed(csv_file, endpoint_url, start_index):

    df = pd.read_csv(csv_file, usecols=["address"], skiprows=range(1, start_index+1))

    # loop over the addresses and hit the endpoint
    for i, address in enumerate(df["address"], start=start_index):
        url = endpoint_url.format(address)

        # handle the response as needed
        # handle the response as needed
        try:
            response = requests.get(url, timeout=300) # wait for a maximum of 5 minutes
            print(f"{bcolors.OKGREEN}Node for address {i}: {address} created successfully{bcolors.ENDC}")
        except requests.Timeout:
            print(f"{bcolors.WARNING}Timed out while waiting for response for address {i}: {address}{bcolors.ENDC}")
        except:
            print(f"{bcolors.FAIL}Failed to create node for address {i}: {address}{bcolors.ENDC}")

if __name__ == "__main__":
    start_index = 99
    seed("./Datasets_Generated/Merged_Datasets/Black_Merged.csv", "http://localhost:5000/project_node/{}", start_index)