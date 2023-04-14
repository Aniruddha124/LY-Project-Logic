from connection import Neo4jConnection

conn = Neo4jConnection(uri="bolt://localhost:7687", user="username", pwd="password")

# project node properties
conn.query("CALL gds.graph.create.cypher('myGraph', 'MATCH (n) RETURN id(n) AS id', 'MATCH (n)-[r]->(m) RETURN id(n) AS source, id(m) AS target, type(r) AS type')")