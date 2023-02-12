import requests
import json

def get_wallet_details(address):
    url = "https://graphql.bitquery.io"

    payload = json.dumps({
    "query": "query ($network: BitcoinNetwork!, $address: String!, $from: ISO8601DateTime, $till: ISO8601DateTime) {\n  bitcoin(network: $network) {\n    inputs(date: {since: $from, till: $till}, inputAddress: {is: $address}) {\n      count\n      value\n      value_usd: value(in: USD)\n      min_date: minimum(of: date)\n      max_date: maximum(of: date)\n    }\n    outputs(date: {since: $from, till: $till}, outputAddress: {is: $address}) {\n      count\n      value\n      value_usd: value(in: USD)\n      min_date: minimum(of: date)\n      max_date: maximum(of: date)\n    }\n  }\n}\n",
    "variables": "{\n  \"limit\": 10,\n  \"offset\": 0,\n  \"network\": \"bitcoin\",\n  \"address\": \""+str(address)+"\",\n  \"from\": \"2020-01-01\",\n  \"till\": \"2023-02-06T23:59:59\",\n  \"dateFormat\": \"%Y-%m-%d\"\n}"
    })
    headers = {
    'Content-Type': 'application/json',
    'X-API-KEY': 'BQYNQXWqKjX4b6WW8l1mMrBorTrUmJAM'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return(response.json())

get_wallet_details("bc1qwukmzzjqn5hwsp4uaswc4c53gc0xz5asrv0prx")