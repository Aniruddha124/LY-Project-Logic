from connection import Neo4jConnection

conn = Neo4jConnection(uri="bolt://localhost:7687", user="username", pwd="password")
conn.query("CREATE OR REPLACE DATABASE coradb")