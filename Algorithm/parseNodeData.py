import json



def parseNodeData(data):
    # Convert the data to the desired format
    nodes = {}
    edges = []
    node_id = 1

    for entry in data['data']:
        start_address = entry['startNode']['address']
        # start_balance = entry['startNode']['balance']
        related_address = entry['relatedNode']['address']
        # related_balance = entry['relatedNode']['balance']
        
        # Check if start node already exists
        if start_address not in nodes:
            # nodes[start_address] = {'id': node_id, 'label': start_address, 'balance': start_balance}
            nodes[start_address] = {'id': node_id, 'label': start_address}
            node_id += 1
        
        # Check if related node already exists
        if related_address not in nodes:
            # nodes[related_address] = {'id': node_id, 'label': related_address, 'balance': related_balance}
            nodes[related_address] = {'id': node_id, 'label': related_address}
            node_id += 1
        
        # Create an edge between the two nodes
        edges.append({'from': nodes[start_address]['id'], 'to': nodes[related_address]['id']})

    # Create the output JSON
    output = {'nodes': list(nodes.values()), 'edges': edges}

    # Print the output
    print(json.dumps(output, indent=2))
    return output

if __name__ == '__main__':
    # Test the function
    data = json.loads('''
        {
        "data": [
            {
            "relatedNode": {
                "address": "21snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm",
                "balance": 1.0
            },
            "startNode": {
                "address": "19snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm",
                "balance": 1.0
            }
            },
            {
            "relatedNode": {
                "address": "20snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm",
                "balance": 2.0
            },
            "startNode": {
                "address": "19snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm",
                "balance": 1.0
            }
            },
            {
            "relatedNode": {
                "address": "19snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm",
                "balance": 1.0
            },
            "startNode": {
                "address": "19snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm",
                "balance": 1.0
            }
            }
        ]
        }
        ''')
    parseNodeData(data)
