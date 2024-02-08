from cassandra.cluster import Cluster

# Define the Cassandra cluster
cassandra_cluster = Cluster(['127.0.0.1'])

# Connect to Cassandra and set keyspace
session = cassandra_cluster.connect()
session.set_keyspace('github_events')

# Define table drop and create queries for Cassandra
table_drop_events = "DROP TABLE IF EXISTS events"
table_drop_actors = "DROP TABLE IF EXISTS actors"

table_create_actors = """
    CREATE TABLE IF NOT EXISTS actors (
        id UUID PRIMARY KEY,
        login TEXT
    )
"""

table_create_events = """
    CREATE TABLE IF NOT EXISTS events (
        id UUID PRIMARY KEY,
        type TEXT,
        actor_id UUID,
        public BOOLEAN,
        FOREIGN KEY(actor_id) REFERENCES actors(id)
    )
"""

cassandra_create_table_queries = [table_create_actors, table_create_events]
cassandra_drop_table_queries = [table_drop_events, table_drop_actors]


def drop_tables(session):
    """
    Drops each table using the queries in `cassandra_drop_table_queries` list.
    """
    for query in cassandra_drop_table_queries:
        session.execute(query)


def create_tables(session):
    """
    Creates each table using the queries in `cassandra_create_table_queries` list.
    """
    for query in cassandra_create_table_queries:
        session.execute(query)


def main():
    """
    - Drops (if exists) and Creates the tables in Cassandra.
    - Finally, closes the connection.
    """
    drop_tables(session)
    create_tables(session)

    # Close Cassandra session and cluster connection
    session.shutdown()
    cassandra_cluster.shutdown()


if __name__ == "__main__":
    main()
