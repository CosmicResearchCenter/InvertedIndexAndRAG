from neo4j import GraphDatabase, Driver, Session

class Neo4jClient:
    def __init__(self, uri: str, username: str, password: str):
        # Initialize connection driver
        self.driver: Driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self) -> None:
        # Close connection
        self.driver.close()

    def create_entity(self, entity: dict) -> None:
        # Creates or updates nodes with the specified labels and properties
        try:
            with self.driver.session() as session:
                entity_label = entity['label'].replace(' ', '')
                properties = ', '.join(f"{k}: ${k}" for k in entity['attribute'].keys())
                match_query = f"MATCH (n:{entity_label} {{ name: $name }}) RETURN n"
                result = session.run(match_query, name=entity['attribute']['name']).single()
                
                if result:
                    # Entity exists, update properties if they have changed
                    set_properties = ', '.join(f"n.{k} = ${k}" for k in entity['attribute'].keys())
                    update_query = f"MERGE (n:{entity_label} {{ name: $name }}) SET {set_properties}"
                    session.run(update_query, **entity['attribute'])
                else:
                    # Entity does not exist, create new entity
                    create_query = f"CREATE (n:{entity_label} {{ {properties} }})"
                    session.run(create_query, **entity['attribute'])
        except KeyError as e:
            print(f"KeyError: {e} key is missing in the entity's attribute dictionary")

    def create_entity_relation(self, entity_relation: dict) -> None:
        # Creates a relationship between two entities
        with self.driver.session() as session:
            query = """
            MATCH (a:%s { name: $name1 }), (b:%s { name: $name2 })
            CREATE (a)-[r:%s]->(b)
            """ % (entity_relation['entity_label1'].replace(" ",""), entity_relation['entity_label2'].replace(" ",""), entity_relation['relation'].replace(" ",""))
            
            session.run(query, name1=entity_relation['name1'].replace(" ",""), name2=entity_relation['name2'].replace(" ",""))