from typing import NewType

import json

import psycopg2


PostgresCursor = NewType("PostgresCursor", psycopg2.extensions.cursor)
PostgresConn = NewType("PostgresConn", psycopg2.extensions.connection)

table_drop_actor = "DROP TABLE IF EXISTS actor CASCADE"
table_drop_repo = "DROP TABLE IF EXISTS repo CASCADE" 
table_drop_issue = "DROP TABLE IF EXISTS issue CASCADE" #FK of payload
table_drop_payload = "DROP TABLE IF EXISTS payload CASCADE"
table_drop_org = "DROP TABLE IF EXISTS org CASCADE"
table_drop_event = "DROP TABLE IF EXISTS event CASCADE"


table_create_actor = """
    CREATE TABLE IF NOT EXISTS actor (
       id bigint ,
       login text,
       display_login text,
       gravatar_id text,
       url text,
       avatar_url text,
       PRIMARY KEY(id)
    )
"""
#Chutimon adds
table_create_repo = """
    CREATE TABLE IF NOT EXISTS repo (
        id int,
        name text,
        url text,
        PRIMARY KEY(id)
    )
"""

table_create_issue = """
    CREATE TABLE IF NOT EXISTS issue (
        url text,
        id int,
        PRIMARY KEY(url)
    )
"""

table_create_payload = """
    CREATE TABLE IF NOT EXISTS payload (
        action text,
        number int,
        push_id int,
        size int,
        distinct_size int,
        ref text,
        ref_type text,
        head text,
        before text,
        master_branch text,
        description text,
        pusher_type text,
        issue_url text, --FK
        PRIMARY KEY(push_id),
        CONSTRAINT fk_issue FOREIGN KEY(issue_url) REFERENCES issue(url)
    )
"""

table_create_org = """
    CREATE TABLE IF NOT EXISTS org (
        id int,
        login text,
        gravatar_id text,
        url text,
        avatar_url text,
        PRIMARY KEY(id)
    )
"""

table_create_event = """
    CREATE TABLE IF NOT EXISTS event (
        id text, 
        type text,
        actor_id int,   --FK
        repo_id int,    --FK
        payload_push_id int, --FK
        public boolean,
        created_at timestamp,
        org_id int,     --FK
        PRIMARY KEY(id),
        CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actor(id),
        CONSTRAINT fk_repo FOREIGN KEY(repo_id) REFERENCES repo(id),
        CONSTRAINT fk_payload FOREIGN KEY(payload_push_id) REFERENCES payload(push_id),
        CONSTRAINT fk_org FOREIGN KEY(org_id) REFERENCES org(id)
    )
"""
    

create_table_queries = [
    table_create_actor,
    table_create_repo,
    table_create_issue,
    table_create_payload,
    table_create_org,
    table_create_event,
]
drop_table_queries = [
    table_drop_actor,
    table_drop_repo,
    table_drop_issue,
    table_drop_payload,
    table_drop_org,
    table_drop_event,
]


def drop_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database.
    - Establishes connection with the sparkify database and gets
    cursor to it.
    - Drops all the tables.
    - Creates all tables needed.
    - Finally, closes the connection.
    """

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()  # connection


    drop_tables(cur, conn)
    # drop_tables(cur, conn) #make loop query (from above) and drop tables (if there is a table)
    # When the user mentions drop_tables, there is no change because of the formula :  CREATE TABLE IF NOT EXISTS actors
    create_tables(cur, conn)  # execute commit

    # summary : drop previous tables and create the new one.
    # TERMINAL : don't click CLT C (Postgres will disappear)

    conn.close()


if __name__ == "__main__":
    main()
