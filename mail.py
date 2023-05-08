import psycopg2

# Функция для создания структуры таблиц.
def create_db(curs):
    curs.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(15),
        surname VARCHAR(20),
        email VARCHAR(100)
        );
    """)
    curs.execute("""
    CREATE TABLE IF NOT EXISTA phones(
        number VARCHAR(11) PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id)
        );
    """)
    return


# Функция внесения номеров телефона.
def insert_phone(curs, client_id, phone):
    