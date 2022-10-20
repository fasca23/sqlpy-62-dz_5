import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE client (
        client_id SERIAL PRIMARY KEY,
        last_name VARCHAR(60) NOT NULL,
        first_name VARCHAR(60) NOT NULL,
        email VARCHAR(60) NOT NULL UNIQUE,
        last_update TIMESTAMP NOT NULL DEFAULT NOW(),
        deleted BOOLEAN DEFAULT FALSE NOT NULL
        );

        CREATE TABLE telephone (
        telephone_id SERIAL PRIMARY KEY,
        telephone INTEGER UNIQUE,
        client_id INTEGER REFERENCES client(client_id),
        last_update TIMESTAMP NOT NULL DEFAULT NOW(),
        deleted BOOLEAN DEFAULT FALSE NOT NULL
        );
                """)
        conn.commit()

def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(last_name, first_name, email) VALUES(%s, %s, %s);
        """, (last_name, first_name, email))
        conn.commit()


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO telephone(client_id, telephone) VALUES(%s, %s);
        """, (client_id, phone))
        conn.commit()


def change_client(conn, client_id, first_name, last_name, email, phone):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE client SET first_name=%s, last_name=%s, email=%s WHERE client_id=%s;
            UPDATE telephone SET telephone=%s WHERE client_id=%s;
            """, (first_name, last_name, email, client_id, phone, client_id))
        conn.commit()


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM telephone WHERE client_id=%s AND telephone=%s;
            """, (client_id, phone))
        conn.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM client WHERE client_id=%s;
            """, (client_id,))
        conn.commit()


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.last_name, c.first_name, c.email, t.telephone 
            FROM client c
            JOIN telephone t ON t.client_id = c.client_id  
            WHERE last_name=%s OR first_name=%s OR email=%s OR telephone=%s
            """, (last_name, first_name, email, phone))
        print(cur.fetchall())


with psycopg2.connect(database="test", user="postgres", password="566133") as conn:
    create_db(conn)
    add_client(conn, 'first_name5', 'last_name5', 'email5')
    add_client(conn, 'first_name6', 'last_name6', 'email6')
    add_client(conn, 'first_name7', 'last_name7', 'email7')
    add_phone(conn, '1', '11117211')
    add_phone(conn, '2', '11142811')
    add_phone(conn, '3', '11133191')
    change_client(conn, client_id='2', first_name='None', last_name='None', email='Non', phone='55558855')
    delete_phone(conn, client_id='1', phone='11117211')
    delete_client(conn, client_id='1')
    find_client(conn, first_name=None, last_name=None, email=None, phone='55558855')
    
conn.close()