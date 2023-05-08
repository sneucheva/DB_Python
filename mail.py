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
    curs.execute("""
        INSERT INTO phones (number, client_id)
        VALUES (%s, %s)
        """, (phone, client_id ))
    return client_id


# Функция для внесения клиентов.
def insert_client(curs, name=None, surname=None, email=None, phone=None):
    curs.execute("""
        INSERT INTO clients(name, surname, email)
        VALUES (%s, %s, %s)
        """, (name, surname, email))
    curs.execute("""
        SELECT id FROM clients
        ORDER BY id DESC
        LIMIT 1
        """)
    id = curs.first()[0]
    if phone is None:
        return id
    else:
        insert_phone(curs, id, phone)
        return id


# Функция измения данных о клиенте.
def update_client(curs, id, name=None, surname=None, email=None):
    curs.execute("""
        SELECT * FROM clients
        WHERE id = %s
        """, (id))
    info = curs.first()
    if name is None:
        name = info[1]
    if surname is None:
        surname = info[2]
    if email is None:
        email = info[3]
    curs.execute("""
        UPDATE clients
        SET name = %s, surname = %s, email = %s
        WHERE id = %s
        """, (name, surname, email, id))
    return id


# Функция удаления телефона.
def delete_phone(curs, number):
    curs.execute("""
        DELETE FROM phones 
        WHWRE number = %s
        """, (number))
    return number


# Функция удаления клиента.
def delete_client(curs, id):
    curs.execute("""
        DELETE FROM phones
        WHERE client_id = %s
        """, (client_id))
    curs.execute("""
        DELETE FROM clients
        WHERE id = %s
        """, (id))
    return id


# Функция поиска клиента.
def find_client(curs, name=None, surname=None, email=None, phone=None):
    if name is None:
        name = '%'
    else:
        name = '%' + name +'%'
    if surname is None:
        surname = '%'
    else:
        surname = '%' + surname +'%'
    if email is None:
        email = '%'
    else:
        email= '%' + email +'%'
    if phone is None:
        curs.execute("""
            SELECT c.id, c.name, c.surname, c.email FROM clients c
            LEFT JOIN phones p ON c.id = p.clients_id
            WHERE c.name LIKE %s AND c.surname LIKE %s AND email LIKE %s
            """, (name, surname, email))
    else:
        curs.execute("""
             SELECT c.id, c.name, c.surname, p.number FROM clients c
             LEFT JOIN phones p ON c.id = p.clients_id
             WHERE c.name LIKE %s AND c.surname LIKE %s AND email LIKE %s AND p.number LIKE %s
             """, (name, surname, email, number))
    return curs.first()


# Проверка работы функций.
with psycopg2.connect(database = "curs", user = "postgres", password = "postgres") as conn:
    with conn.cursor() as cur:
        create_db(curs)
        insert_client(curs, "Ivan", "Ivanov", "ivanov@gmail.com")
        insert_client(curs, "Petr", "Petrov", "petrov@mail.ru", 79113867314)
        insert_phone(curs, 1, 79213456450)
        update_client(curs, None, None, "ivanco@yandex.ru")
        delete_phone(curs, 79113867314)
        delete_client(curs, 2)


