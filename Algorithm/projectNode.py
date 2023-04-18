from connection import Neo4jConnection
import re
import json
from FetchAssociatedAddress import get_associated_addresses

async def node_exists(conn,address):
    result = conn.query(f'''
    MATCH (a:Entity)
    WHERE a.address = '{address}'
    RETURN a''',
        db='verdb-test'
    )

    return len(result) > 0


async def relationship_exists(conn, start_address, end_address):
    result = conn.query(f'''
    MATCH (a:Entity)-[r]-(b:Entity)
    WHERE a.address = '{start_address}' AND b.address = '{end_address}'
    RETURN r''',
        db='verdb-test'
    )
    return len(result) > 0

def project_node(address):
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")

    # check if address node exists
    if node_exists(conn, address):
        print("Node exists")
    else:
        print("Node does not exist")
        conn.query("MERGE(a:Entity {address: "+address+"})")
        print(f"Node {address} created")

    
    associated_addresses = await get_associated_addresses(address)

    # remove address from associated addresses
    if len(associated_addresses) > 0:
        associated_addresses.remove(address)

    for associated_address in associated_addresses:
        # check if associated address node exists
        if node_exists(conn, associated_address):
            print(f"Associated Node {associated_address} exists")
        else:
            print(f"Associated Node {associated_address} does not exist")
            await conn.query("MERGE(a:Entity {address: "+associated_address+"})")
            print(f"Associated Node {associated_address} created")

        # check if relationship exists
        for associated_address in associated_addresses:
            if relationship_exists(conn, address, associated_address):
                print(f"Relationship between {address} and {associated_address} exists")
            else:
                print(f"Relationship between {address} and {associated_address} does not exist")
                await conn.query(f"MERGE (a:Entity {{address: '{address}'}})-[r:LINK]->(b:Entity {{address: '{associated_address}'}})")
                print(f"Relationship between {address} and {associated_address} created")

    # fetching updated node data
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

if __name__ == "__main__":
    print(project_node("19snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm"))
    
    # conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")
    # print(node_exists(conn,"2snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm"))
    # print(relationship_exists(conn,"19snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm","2snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm"))

