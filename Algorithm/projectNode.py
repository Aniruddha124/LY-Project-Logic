from connection import Neo4jConnection
import re
import json

def node_exists(conn,address):
    result = conn.query(f'''
    MATCH (a:Entity)
    WHERE a.address = '19snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm'
    RETURN a''',
        db='verdb-test'
    )
    return result.single() is not None

def project_node(address):
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")

    # check if address node exists
    if node_exists(conn, address):
        print("Node exists")
    else:
        print("Node does not exist")
        conn.query("MERGE(a:Entity {address: "+address+"})")
        print("Node created")
    
    