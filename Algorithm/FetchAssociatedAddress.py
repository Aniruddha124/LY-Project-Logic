import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
BITQUERY_API_KEY =  os.getenv("BITQUERY_API_KEY")
url = "https://graphql.bitquery.io"

async def get_tx_addresses(tx_hash):
    payload = json.dumps({
   "query": " query ($tx_hash: String!) {\n  bitcoin {\n    inputs(\n      txHash: {is: $tx_hash}\n    ) {\n      inputAddress {\n        address\n      }\n    }\n  }\n}",
   "variables": f"{{\n  \"tx_hash\": \"{tx_hash}\"\n}}"
    })
    headers = {
    'Content-Type': 'application/json',
    'X-API-KEY': BITQUERY_API_KEY
    }

    addresses_involved = []
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except:
        print("Error")
    
    for address in response.json()["data"]["bitcoin"]["inputs"]:
        addresses_involved.append(address["inputAddress"]["address"])
    
    return addresses_involved
    



async def get_associated_addresses(address):
    payload = json.dumps({
    "query": "query ($address: String!) {\n  bitcoin {\n    transactions(\n      any: {inputAddress: {is: $address}}\n    ) {\n      hash\n    }\n  }\n}",
    "variables": f"{{\n  \"address\": \"{address}\"\n}}"
    })
    headers = {
    'Content-Type': 'application/json',
    'X-API-KEY': BITQUERY_API_KEY
    }

    # fetching tx data for addresses
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except:
        print("Error")
    
    tx_list = []
    for tx in response.json()["data"]["bitcoin"]["transactions"]:
        tx_list.append(tx["hash"])
    # print(tx_list)


    associated_addresses = []
    # fetching addresses from tx data
    for tx_hash in tx_list:
        addresses_involved = await get_tx_addresses(tx_hash)
        associated_addresses.extend(addresses_involved)
    
    final_addresses = list(set(associated_addresses))
    print(final_addresses)
    return final_addresses

if __name__ == "__main__":
    get_associated_addresses("bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh")
    # print(get_tx_addresses("053fe44233d8e8a625d509f0dcf6aef672f297b4c2c7d7bd989d377027888b56"))