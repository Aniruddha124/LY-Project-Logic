import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
BITQUERY_API_KEY = os.getenv("BITQUERY_API_KEY")
url = "https://graphql.bitquery.io"


def get_address_details(public_address, inboundDepth=1, outboundDepth=1, limit=500, offset=0, network="bitcoin", fromValue="null", tillValue="null", dateFormat="%Y-%m"):
    payload = json.dumps({
        "query": "query MyQuery($public_address: String!, $inboundDepth: Int!, $outboundDepth: Int!, $limit: Int!, $fromValue: ISO8601DateTime, $tillValue: ISO8601DateTime) {\n  bitcoin {\n    address_stats: addressStats(address: {is: $public_address}) {\n      address {\n        balance\n        inboundTransactions\n        outboundTransactions\n        inflows\n        outflows\n        uniqueReceivers\n        uniqueSenders\n        firstActive {\n          iso8601\n        }\n        lastActive {\n          iso8601\n        }\n      }\n    }\n    incoming_transactions: coinpath(\n      initialAddress: {is: $public_address}\n      depth: {lteq: $inboundDepth}\n      options: {direction: inbound, asc: \"depth\", desc: \"amount\", limitBy: {each: \"depth\", limit: $limit}}\n      date: {since: $fromValue, till: $tillValue}\n    ) {\n      sender {\n        address\n        annotation\n      }\n      receiver {\n        address\n        annotation\n      }\n      amount\n      depth\n      count\n      transaction {\n        hash\n      }\n      transaction_more_info: transactions {\n        timestamp\n      }\n    }\n    outgoing_transactions: coinpath(\n      initialAddress: {is: $public_address}\n      depth: {lteq: $outboundDepth}\n      options: {asc: \"depth\", desc: \"amount\", limitBy: {each: \"depth\", limit: $limit}}\n      date: {since: $fromValue, till: $tillValue}\n    ) {\n      sender {\n        address\n        annotation\n      }\n      receiver {\n        address\n        annotation\n      }\n      amount\n      depth\n      count\n      transaction {\n        hash\n      }\n      transaction_more_info: transactions {\n        timestamp\n      }\n    }\n  }\n}\n",
        "variables": f"{{\n  \"public_address\": \"{public_address}\",\n   \"inboundDepth\": {int(inboundDepth)},\n  \"outboundDepth\": {int(outboundDepth)},\n  \"limit\": {int(limit)},\n  \"offset\": {int(offset)},\n  \"network\": \"bitcoin\",\n  \"fromValue\": {fromValue},\n  \"tillValue\": {tillValue},\n  \"dateFormat\": \"{dateFormat}\"\n}}"
    })
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': BITQUERY_API_KEY
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except requests.exceptions as e:
        print("Error ", e)

    print(response.text)


get_address_details("35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP")
