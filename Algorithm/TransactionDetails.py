import requests
import json

def get_transaction_details(address):
    url = "https://graphql.bitquery.io"

    payload = json.dumps({
   "query": "query ($network: BitcoinNetwork!, $address: String!, $limit: Int!, $offset: Int!, $from: ISO8601DateTime, $till: ISO8601DateTime) {\n  bitcoin(network: $network) {\n    inputs(\n      date: {since: $from, till: $till}\n      inputAddress: {is: $address}\n      options: {desc: [\"block.height\", \"transaction.index\"], limit: $limit, offset: $offset}\n    ) {\n      block {\n        height\n        timestamp {\n          time(format: \"%Y-%m-%d %H:%M:%S\")\n        }\n      }\n      transaction {\n        hash\n        index\n      }\n      value\n      value_usd: value(in: USD)\n    }\n    outputs(\n      date: {since: $from, till: $till}\n      outputAddress: {is: $address}\n      options: {desc: [\"block.height\", \"transaction.index\"], limit: $limit, offset: $offset}\n    ) {\n      block {\n        height\n        timestamp {\n          time(format: \"%Y-%m-%d %H:%M:%S\")\n        }\n      }\n      transaction {\n        hash\n        index\n      }\n      value\n      value_usd: value(in: USD)\n    }\n  }\n}\n",
   "variables": "{\n  \"limit\": 10,\n  \"offset\": 0,\n  \"address\": \""+str(address)+"\",\n  \"network\": \"bitcoin\",\n  \"from\": \"2009-01-30\",\n  \"till\": \"2023-02-06T23:59:59\",\n  \"dateFormat\": \"%Y-%m-%d\"\n}"
})
    
    headers = {
    'Content-Type': 'application/json',
    'X-API-KEY': 'BQYNQXWqKjX4b6WW8l1mMrBorTrUmJAM'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    return(response.json())

# get_transaction_details("bc1qwukmzzjqn5hwsp4uaswc4c53gc0xz5asrv0prx")