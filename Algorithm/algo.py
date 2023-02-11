import json

# read json file
with open('dummy.json') as f:
    data = json.load(f)
    # print(data)
    in_degree = len(data['bitcoin']['inbound'])
    out_degree = len(data['bitcoin']['outbound'])
    print(in_degree)
    print(out_degree)

# creating a table for transactions
