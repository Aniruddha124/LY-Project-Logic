from connection import Neo4jConnection

conn = Neo4jConnection(uri="bolt://localhost:7687", user="username", pwd="password")
# create new node
conn.query("CREATE (n:Person {name: 'Bob', age: 42})")