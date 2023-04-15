from connection import Neo4jConnection


def fetch_node(address):
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="username", pwd="password")

    # return associated nodes
    return conn.query('''
        MATCH (startNode)-[*]-(relatedNode)
        WHERE startNode.address = {address}
        RETURN DISTINCT startNode, relatedNode'''
    )
    