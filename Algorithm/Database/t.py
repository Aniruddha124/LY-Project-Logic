from connection import Neo4jConnection

conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")
try:
    print(conn.query('''MATCH (a:Entity {address: '2snqSYnDSC4mDbv3pJuYgYqm5ctqwAxnm'})
    RETURN a''',db="verdb-test")[0].data())
except:
    print("No such node")

