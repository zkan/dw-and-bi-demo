
import glob
import json
import os
from typing import List

import psycopg2


def get_files(filepath: str) -> List[str]:
    """
    Description: This function is responsible for listing the files in a directory
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    return all_files


def process(cur, conn, filepath):
    # Get list of files from filepath
    all_files = get_files(filepath)

    for datafile in all_files:
        with open(datafile, "r") as f:
            data = json.loads(f.read())
            for each in data:
                # Print some sample data
                
                if each["type"] == "IssueCommentEvent":
                    print(
                        each["id"], 
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["created_at"],
                        each["payload"]["issue"]["url"],
                    )
                else:
                    print(
                        each["id"], 
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["created_at"],
                    )

                # 1. Insert actor data into tables here
                insert_statement = f"""
                    INSERT INTO actor (
                        id,
                        login,
                        display_login,
                        gravatar_id, 
                        url, 
                        avatar_url
                    ) VALUES ({each["actor"]["id"]},
                              '{each["actor"]["login"]}',
                              '{each["actor"]["display_login"]}', 
                              '{each["actor"]["gravatar_id"]}',
                              '{each["actor"]["url"]}',
                              '{each["actor"]["avatar_url"]}')
                    ON CONFLICT (id) DO NOTHING;
                """
                # print(insert_statement)
                cur.execute(insert_statement)

                # 2. Insert repo data into tables here
                insert_statement = f"""
                    INSERT INTO repo (
                        id,
                        name,
                        url
                    ) VALUES ({each["repo"]["id"]},
                              '{each["repo"]["name"]}',
                              '{each["repo"]["url"]}')
                    ON CONFLICT (id) DO NOTHING;
                """
                # print(insert_statement)
                cur.execute(insert_statement)

                # 3. Insert issue data into tables here

                # 4. Insert payload data into tables here

                # 5. Insert org data into tables here

                # 6. Insert event data into tables here

                insert_statement = f"""
                    INSERT INTO event (
                        id, 
                        type,
                        actor_id,
                        repo_id,
                        public,
                        created_at
                    ) VALUES ('{each["id"]}', '{each["type"]}', '{each["actor"]["id"]}', '{each["repo"]["id"]}',
                             {'True' if each["public"] else 'False'}, '{each["created_at"]}')
                    ON CONFLICT (id) DO NOTHING;
                """
                # print(insert_statement)
                cur.execute(insert_statement)

                conn.commit()


def main():
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor() #Create the connection

    process(cur, conn, filepath="../data") #Request the functional process

    conn.close() #Close the connection


if __name__ == "__main__":
    main()