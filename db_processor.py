import psycopg2

def insert(id: int, name: str, age: int, conn):
    cur = conn.cursor()
    cur.execute("INSERT INTO bot (id, name, age) VALUES (%s, %s, %s)", (id, name, age))
    conn.commit()
    cur.close()

def select(id: int, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM bot WHERE id = (%s)", (id,))
    answer = cur.fetchall()
    return answer
    for elem in answer:
        print("Id = ", elem[0])
        print("Имя = ", elem[1])
        print("Возраст  = ", elem[2], "\n")
    cur.close()

def select_all(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM bot ORDER BY id")
    answer = cur.fetchall()
    return answer
    for elem in answer:
        print("Id = ", elem[0])
        print("Имя = ", elem[1])
        print("Возраст  = ", elem[2], "\n")
    cur.close()

def update(id: int, name: str, age: int, conn):
    cur = conn.cursor()
    cur.execute("UPDATE bot SET name = (%s), age = (%s) WHERE id = (%s)", (name, age, id))
    conn.commit()
    cur.close()

def delete(id: int, conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM bot WHERE id = (%s)", (id,))
    conn.commit()
    cur.close()