from connection import Neo4jConnection
import re
import json

def fetch_node(address):
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")
    print(address)
    # return associated nodes
    data = conn.query(f'''
        MATCH (startNode)-[*]-(relatedNode)
        WHERE startNode.address = '{address}'
        RETURN DISTINCT startNode, relatedNode''',
        db='verdb-test'
    )
    results = []
    for i in range(len(data)):
        results.append(data[i].data())

    return {
        "data": results 
    }
    