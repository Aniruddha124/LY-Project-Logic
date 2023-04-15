from connection import Neo4jConnection
conn = Neo4jConnection(uri="bolt://localhost:7687", 
                       user="neo4j",              
                       pwd="12345678")
conn.query("CREATE OR REPLACE DATABASE newdb")