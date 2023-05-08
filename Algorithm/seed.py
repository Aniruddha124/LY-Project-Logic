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

def seed(csv_file, endpoint_url):

    df = pd.read_csv(csv_file, usecols=["address"])

    # loop over the addresses and hit the endpoint
    for address in df["address"]:
        url = endpoint_url.format(address)
        response = requests.get(url)

        # handle the response as needed
        if response.status_code == 200:
            print(f"{bcolors.OKGREEN}Node for {address} created successfully{bcolors.ENDC}")
        else:
            print(f"{bcolors.FAIL}Failed to create node for {address}{bcolors.ENDC}")


if __name__ == "__main__":
    seed("./Datasets_Generated/Merged_Datasets/Black_Merged.csv", "http://localhost:5000/project_node/{}")