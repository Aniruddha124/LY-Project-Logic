from connection import Neo4jConnection
import re
import json
import asyncio
from FetchAssociatedAddress import get_associated_addresses
from Score import Score

async def create_node(conn, address, score):
    conn.query(f"MERGE(a:Entity {{address: '{address}', score: '{score}'}})", db='verdb')
    return True

async def update_node(conn, address, score):
    conn.query(f"MATCH(a:Entity {{address: '{address}'}}) SET a.score = '{score}'", db='verdb')
    return True

async def create_relationship(conn, start_address, end_address):
    conn.query(f'''
    MATCH (a:Entity),(b:Entity)
    WHERE a.address = '{start_address}' AND b.address = '{end_address}'
    MERGE (a)-[r:LINK]->(b)
    RETURN type(r)''',
        db='verdb'
    )
    return True

async def node_exists(conn,address):
    result = conn.query(f'''
    MATCH (a:Entity)
    WHERE a.address = '{address}'
    RETURN a''',
        db='verdb'
    )

    return len(result) > 0


async def relationship_exists(conn, start_address, end_address):
    result = conn.query(f'''
    MATCH (a:Entity)-[r]-(b:Entity)
    WHERE a.address = '{start_address}' AND b.address = '{end_address}'
    RETURN r''',
        db='verdb'
    )
    return len(result) > 0

async def fetch_data(conn, address):
    print("fetching..")
    data = conn.query(f'''
        MATCH (startNode)-[*..10]-(relatedNode)
        WHERE startNode.address = '{address}'
        RETURN DISTINCT startNode, relatedNode''',
        db='verdb'
    )
    return data 

async def project_node(address):
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")

    score = Score(address)['score']
    # score = 2 # while seeding
    

    # check if address node exists
    if await node_exists(conn, address):
        print("Node exists")
        await update_node(conn,address,score)
    else:
        print("Node does not exist")
        await create_node(conn, address, score)
        # await conn.query(f"MERGE(a:Entity {{address: '{address}'}})",db='verdb-test')
        print(f"Node {address} created")

    
    associated_addresses = await get_associated_addresses(address)

    # remove address from associated addresses
    if len(associated_addresses) > 0:
        associated_addresses.remove(address)

        for associated_address in associated_addresses:
            # check if associated address node exists
            if await node_exists(conn, associated_address):
                print(f"Associated Node {associated_address} exists")
            else:
                print(f"Associated Node {associated_address} does not exist")
                await create_node(conn, associated_address, -1)
                print(f"Relationship between {address} and {associated_address} created")
                

            # check if relationship exists
            for associated_address in associated_addresses:
                if await relationship_exists(conn, address, associated_address):
                    print(f"Relationship between {address} and {associated_address} exists")
                else:
                    print(f"Relationship between {address} and {associated_address} does not exist")
                    await create_relationship(conn,address,associated_address)
                    print(f"Relationship between {address} and {associated_address} created")
                    
    print("projection complete ")
    # fetching updated node data
    data = await fetch_data(conn, address)
    conn.close()
    results = []
    for i in range(len(data)):
        results.append(data[i].data())
    print(results)
    return {
        "data": results 
    }

if __name__ == "__main__":
    # conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")
    # print(node_exists(conn,"2snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm"))
    # print(relationship_exists(conn,"19snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm","2snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm"))

    asyncio.run(project_node("1NDStkokJ9EL7P8SV2HUv6qzLZw8vdEZPv"))
