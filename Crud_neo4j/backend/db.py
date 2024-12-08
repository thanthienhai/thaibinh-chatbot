from neo4j import GraphDatabase

# Update with your Neo4j credentials and host
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "test"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def create_file(tx, file_id, filename):
    tx.run(
        """
        CREATE (f:File {file_id: $file_id, filename: $filename, upload_date: datetime()})
        """,
        file_id=file_id,
        filename=filename
    )

def create_chunk(tx, file_id, chunk_id, text, order):
    tx.run(
        """
        MATCH (f:File {file_id: $file_id})
        CREATE (c:Chunk {chunk_id: $chunk_id, text: $text, order: $order})
        MERGE (f)-[:HAS_CHUNK]->(c)
        """,
        file_id=file_id,
        chunk_id=chunk_id,
        text=text,
        order=order
    )

def link_chunks(tx):
    # This will link chunks within each file based on their order
    # This query finds all chunks of a file ordered by order, then creates NEXT/PREV relationships
    tx.run(
        """
        MATCH (f:File)-[:HAS_CHUNK]->(c:Chunk)
        WITH f, c ORDER BY f.file_id, c.order
        WITH f, collect(c) as chunks
        UNWIND range(0, size(chunks)-2) AS i
        WITH chunks[i] as c1, chunks[i+1] as c2
        CREATE (c1)-[:NEXT]->(c2)
        CREATE (c2)-[:PREV]->(c1)
        """
    )

def list_files(tx):
    result = tx.run("MATCH (f:File) RETURN f.file_id as file_id, f.filename as filename, f.upload_date as upload_date ORDER BY f.upload_date DESC")
    return [r.data() for r in result]

def get_chunks(tx, file_id):
    result = tx.run(
        "MATCH (f:File {file_id: $file_id})-[:HAS_CHUNK]->(c:Chunk) RETURN c.chunk_id as chunk_id, c.text as text, c.order as order ORDER BY c.order",
        file_id=file_id
    )
    return [r.data() for r in result]

def delete_file(tx, file_id):
    # Delete the file and its chunks
    tx.run(
        """
        MATCH (f:File {file_id: $file_id})-[*0..]->(n)
        DETACH DELETE f, n
        """,
        file_id=file_id
    )