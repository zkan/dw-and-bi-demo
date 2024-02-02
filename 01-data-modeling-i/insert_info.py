import json
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Load JSON data from the file
with open('github_events_01.json', 'r') as file:
    data = json.load(file)

# Iterate over the data and insert into the actor table
for entry in data:
    actor_data = (
        entry.get('id', None),
        entry.get('login', None),
        entry.get('display_login', None),
        entry.get('gravatar_id',None),
        entry.get('url', None),
        entry.get('avatar_url', None)
    )

    # SQL INSERT statement for the actor table
    sql_insert_actor = "INSERT INTO actor (id, login, display_login, gravatar_id, url, avatar_url) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING"

    # Execute the SQL INSERT statement
    cur.execute(sql_insert_actor, actor_data)

# Commit the changes to the database
conn.commit()


# Close the cursor and the database connection
cur.close()
conn.close()
