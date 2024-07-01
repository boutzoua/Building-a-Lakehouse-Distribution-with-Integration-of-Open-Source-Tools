import psycopg2
from datetime import datetime
import random

def insert_user_data(conn, users):
    query = "INSERT INTO users (id, first_name, last_name, job_title, salary, company, location) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor=conn.cursor()
    cursor.executemany(query, users)
    cursor.close()
    conn.commit()

# Function to update user data
def update_user_data(conn, update_col, new_value, predicate):
    query = f"Update users set {update_col}='{new_value}' where {predicate};"
    cursor=conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()

#Function to delete user records basing on a predicate
def delete_user_data(conn, predicate):
    query=f"Delete from users where {predicate};"
    cursor=conn.cursor()
    cursor.execute(query)
    cursor.close()
    conn.commit()

if __name__ == "__main__":
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='postgres',
        port=5433
    )

    try:
        users_data=[]
        insert_user_data(conn, users_data)
        print("User data inserted successfully!")
        # to_update = [("Date",""),("Adj Close",""),
        #          ("",""),("","")]
        # for update_col, new_value in to_update:
        #     update_user_data(conn,update_col, new_value, "id=11")
        #     print("User data updated successfully!")
        
        # for id in range(1,11):
        #     cursor = conn.cursor()
        #     cursor.execute(f"Delete from users where id={id}")
        #     print(f"User with {id=} deleted successfully!")
        #     cursor.close()
        #     conn.commit()
    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()