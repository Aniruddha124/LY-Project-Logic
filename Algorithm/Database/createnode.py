from connection import Neo4jConnection

conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")
# create new node
conn.query("CREATE (n:Person {name: 'Bob', age: 42})", db='newdb')