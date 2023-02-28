import requests
import json

url = "https://graphql.bitquery.io/"

{
  "inboundDepth": 1,
  "outboundDepth": 1,
  "limit": 100,
  "offset": 0,
  "network": "bitcoin",
  "address": "18E1sRX2aXySM1y1AYC9p3wFy19C7t8wx",
  "from": null,
  "till": null,
  "dateFormat": "%Y-%m"
}

payload = json.dumps({
    "query": "query ($network: BitcoinNetwork!, $address: String!, $inboundDepth: Int!, $outboundDepth: Int!, $limit: Int!, $from: ISO8601DateTime, $till: ISO8601DateTime) {\n  bitcoin(network: $network) {\n    incoming_transactions: coinpath(\n      initialAddress: {is: $address}\n      depth: {lteq: $inboundDepth}\n      options: {direction: inbound, asc: "depth", desc: "amount", limitBy: {each: "depth", limit: $limit}}\n      date: {since: $from, till: $till}\n    ) {\n      sender {\n        address\n        annotation\n      }\n      receiver {\n        address\n        annotation\n      }\n      amount\n      depth\n      count\n    }\n    outgoing_transactions: coinpath(\n      initialAddress: {is: $address}\n      depth: {lteq: $outboundDepth}\n      options: {asc: "depth", desc: "amount", limitBy: {each: "depth", limit: $limit}}\n      date: {since: $from, till: $till}\n    ) {\n      sender {\n        address\n        annotation\n      }\n      receiver {\n        address\n        annotation\n      }\n      amount\n      depth\n      count\n    }\n  }\n}\n",
    "variables": "{\n  "inboundDepth": 1,\n  "outboundDepth": 1,\n  "limit": 100,\n  "offset": 0,\n  "network": "bitcoin",\n  "address": "18E1sRX2aXySM1y1AYC9p3wFy19C7t8wx",\n  "from": null,\n  "till": null,\n  "dateFormat": "%Y-%m"\n}"
})
headers = {
    'Content-Type': 'application/json',
    'X-API-KEY': 'BQY3GRjX77tiVINrz3JT7X8LxFFGoYf5'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)