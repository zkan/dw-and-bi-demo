from typing import NewType

import json

import psycopg2


PostgresCursor = NewType("PostgresCursor", psycopg2.extensions.cursor)
PostgresConn = NewType("PostgresConn", psycopg2.extensions.connection)

table_drop_event = "DROP TABLE IF EXISTS event CASCADE" #connect to actors
table_drop_actor = "DROP TABLE IF EXISTS actor CASCADE" #main
#Chutimon adds
table_drop_repository = "DROP TABLE IF EXISTS reposity" 
table_drop_issue = "DROP TABLE IF EXISTS issue CASCADE"
table_drop_issue_comments = "DROP TABLE IF EXISTS issue_comments CASCADE"
table_drop_reactions = "DROP TABLE IF EXISTS reactions"


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
table_create_repository = """
    CREATE TABLE IF NOT EXISTS repository (
        id int,
        type text,
        URL text,
        PRIMARY KEY(id)
    )
"""
table_create_issue = """
    CREATE TABLE IF NOT EXISTS issue (
        id int,
        url text,
        repository_url text, --FK
        labels_url text,
        comment_url text,   --FK
        event_url text,     --FK
        html_url text,
        number int,
        title text,
        user_id int,
        state text,
        locked boolean,
        assignee_id int,
        milestone_url text,
        comments int,
        created_at timestamp,
        updated_at timestamp,
        closed_at timestamp,
        author_association text,
        active_lock_reason text,
        body text,
        PRIMARY KEY(id)
    )
"""

table_create_issue_comments = """
    CREATE TABLE IF NOT EXISTS issue_comments (
        id int,
        url text,
        html_url text,
        issue_url text,
        user_id int,
        created_at timestamp,
        updated_at timestamp,
        author_association text,
        body text,
        PRIMARY KEY(id)
    )
"""

table_create_reactions = """ 
    CREATE TABLE IF NOT EXISTS reactions (
        id int,
        issues_id int,   --FK
        comment_id int,  --FK
        user_id int,
        reaction_type text,
        created_at timestamp,
        PRIMARY KEY(id),
        CONSTRAINT fk_issues FOREIGN KEY(issues_id) REFERENCES issue(id),
        CONSTRAINT fk_issue FOREIGN KEY(comment_id) REFERENCES issue_comments(id)
)
"""

table_create_event = """
    CREATE TABLE IF NOT EXISTS event (
        id text, 
        type text,
        created_at timestamp,
        public boolean,
        payload_action text,
        actor_id int,   --FK
        repo_id int,    --FK
        comment_id int, --FK
        PRIMARY KEY(id),
        CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actor(id),
        CONSTRAINT fk_repository FOREIGN KEY(repo_id) REFERENCES repository(id),
        CONSTRAINT fk_issue FOREIGN KEY(comment_id) REFERENCES issue_comments(id)
    )
"""
    

create_table_queries = [
    table_create_actor,
    table_create_repository,
    table_create_issue,
    table_create_issue_comments,
    table_create_reactions,
    table_create_event,
]
drop_table_queries = [
    table_drop_actor,
    table_drop_repository,
    table_drop_issue,
    table_drop_issue_comments,
    table_drop_reactions,
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
