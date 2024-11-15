from neo4j import GraphDatabase, Driver, Session

class Neo4jClient:
    def __init__(self, uri: str, username: str, password: str):
        # Initialize connection driver
        self.driver: Driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self) -> None:
        # Close connection
        self.driver.close()

    def create_entity(self, entity: dict) -> None:
        # Creates nodes with the specified labels and properties
        with self.driver.session() as session:
            entity_label = entity['label'].replace(' ', '')
            properties = ', '.join(f"{k}: ${k}" for k in entity['attribute'].keys())
            query = f"CREATE (n:{entity_label} {{ {properties} }})"
            session.run(query, **entity['attribute'])

    def create_entity_relation(self, entity_relation: dict) -> None:
        # Creates a relationship between two entities
        with self.driver.session() as session:
            query = """
            MATCH (a:%s { name: $name1 }), (b:%s { name: $name2 })
            CREATE (a)-[r:%s]->(b)
            """ % (entity_relation['entity_label1'], entity_relation['entity_label2'], entity_relation['relation'])
            
            session.run(query, name1=entity_relation['name1'], name2=entity_relation['name2'])

