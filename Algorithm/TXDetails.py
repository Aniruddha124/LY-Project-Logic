import requests
import json

def get_complete_tx_details(address):
    url = "https://graphql.bitquery.io"

    payload = json.dumps({
   "query": "query ($network: BitcoinNetwork!, $address: String!, $inboundDepth: Int!, $outboundDepth: Int!, $limit: Int!, $from: ISO8601DateTime, $till: ISO8601DateTime) {\n  bitcoin(network: $network) {\n    inbound: coinpath(\n      initialAddress: {is: $address}\n      depth: {lteq: $inboundDepth}\n      options: {direction: inbound, asc: \"depth\", desc: \"amount\", limitBy: {each: \"depth\", limit: $limit}}\n      date: {since: $from, till: $till}\n    ) {\n      sender {\n        address\n        annotation\n      }\n      receiver {\n        address\n        annotation\n      }\n      amount\n      depth\n      count\n    }\n    outbound: coinpath(\n      initialAddress: {is: $address}\n      depth: {lteq: $outboundDepth}\n      options: {asc: \"depth\", desc: \"amount\", limitBy: {each: \"depth\", limit: $limit}}\n      date: {since: $from, till: $till}\n    ) {\n      sender {\n        address\n        annotation\n      }\n      receiver {\n        address\n        annotation\n      }\n      amount\n      depth\n      count\n    }\n  }\n}\n",
   "variables": "{\n  \"inboundDepth\": 1,\n  \"outboundDepth\": 1,\n  \"limit\": 100,\n  \"offset\": 0,\n  \"network\": \"bitcoin\",\n  \"address\": \""+str(address)+"\",\n  \"from\": null,\n  \"till\": null,\n  \"dateFormat\": \"%Y-%m\"\n}"
})
    headers = {
    'Content-Type': 'application/json',
    'X-API-KEY': 'BQYNQXWqKjX4b6WW8l1mMrBorTrUmJAM'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    return(response.json())

# get_complete_tx_details("bc1qwukmzzjqn5hwsp4uaswc4c53gc0xz5asrv0prx")