from connection import Neo4jConnection

conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")

# project node properties
query = '''CALL gds.graph.project(
  graphName: my-graph,
  nodeProjection: String or List or Map,
  relationshipProjection: String or List or Map,
  configuration: Map
) YIELD
  graphName: String,
  nodeProjection: Map,
  nodeCount: Integer,
  relationshipProjection: Map,
  relationshipCount: Integer,
  projectMillis: Integer'''

conn.query(query,db='newdb')

