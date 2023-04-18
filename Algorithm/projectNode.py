from connection import Neo4jConnection
import re
import json
import asyncio
from FetchAssociatedAddress import get_associated_addresses

async def create_node(conn, address):
    conn.query(f"MERGE(a:Entity {{address: '{address}'}})", db='verdb-test')
    return True

# async def create_node(conn, address):
#     conn.query(f"MERGE(a:Entity) a.address= '{address}'", db='verdb-test')
#     return True

async def create_relationship(conn, start_address, end_address):
    conn.query(f'''
    MATCH (a:Entity),(b:Entity)
    WHERE a.address = '{start_address}' AND b.address = '{end_address}'
    MERGE (a)-[r:LINK]->(b)
    RETURN type(r)''',
        db='verdb-test'
    )
    return True

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

async def project_node(address):
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")

    # check if address node exists
    if await node_exists(conn, address):
        print("Node exists")
    else:
        print("Node does not exist")
        await create_node(conn, address)
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
                await create_node(conn, associated_address)
                # try:
                #     await create_node(conn, address)
                #     print(f"Associated Node {associated_address} created")
                # except:
                #     print("Could not create node.")
                #     continue
                # await conn.query(f"MERGE(a:Entity {{address: '{associated_address}'}})", db='verdb-test')
                

            # check if relationship exists
            for associated_address in associated_addresses:
                if await relationship_exists(conn, address, associated_address):
                    print(f"Relationship between {address} and {associated_address} exists")
                else:
                    print(f"Relationship between {address} and {associated_address} does not exist")
                    await create_relationship(conn,address,associated_address)
                    # try:
                    #     await create_relationship(conn,address,associated_address)
                    #     print(f"Relationship between {address} and {associated_address} created")
                    # except:
                    #     print("Could not create relationship.")
                    #     continue
                    # await conn.query(f"MERGE (a:Entity {{address: '{address}'}})-[r:LINK]->(b:Entity {{address: '{associated_address}'}})", db='verdb-test')
                    

    
    # fetching updated node data
    data = conn.query(f'''
        MATCH (startNode)-[*]-(relatedNode)
        WHERE startNode.address = '{address}'
        RETURN DISTINCT startNode, relatedNode''',
        db='verdb-test'
    )
    conn.close()
    results = []
    for i in range(len(data)):
        results.append(data[i].data())
    print(results)
    return {
        "data": results 
    }

if __name__ == "__main__":
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")
    address = '35snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm'
    # associated_address = "30snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm"
    # print(conn.query(f"MERGE(a:Entity {{address: '{address}'}})", db='verdb-test'))

    # print(conn.query(f"MERGE(a:Entity)a.address= '{address}'", db='verdb-test'))
    # print(conn.query('''MATCH (startNode)-[*]-(relatedNode)
    #     WHERE startNode.address = '19snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm'
    #     RETURN DISTINCT startNode, relatedNode''', db = "verdb-test"))

    asyncio.run(project_node("bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"))

    # print(await project_node("19snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm"))
    
    # conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")
    # print(node_exists(conn,"2snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm"))
    # print(relationship_exists(conn,"19snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm","2snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm"))

