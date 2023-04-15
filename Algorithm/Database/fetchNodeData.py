from connection import Neo4jConnection


def fetch_node(address):
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="12345678")

    # return associated nodes
    return conn.query('''
        MATCH (startNode)-[*]-(relatedNode)
        WHERE startNode.address = {address}
        RETURN DISTINCT startNode, relatedNode'''
    )
    