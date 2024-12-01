import psycopg2


def created_data_base(cursor, config_create):
    return cursor.execute(config_create)


def insertclient(cursor, name, surname, email):
    return cursor.execute("""INSERT INTO Client (name, surname, Email)
                          values(%s, %s, %s);""", (name, surname, email,))


def insertphone(cursor, idclient, phone):
    return cursor.execute("""INSERT INTO Phone (idclient, phone)
                             values(%s ,%s)""", (idclient, phone,))


def updateclient(cursor, ids, name=None, surname=None, email=None):

    query = "UPDATE client SET "
    params = []

    if name is not None:
        query += "name = %s, "
        params.append(name)
    if surname is not None:
        query += "surname = %s, "
        params.append(surname)
    if email is not None:
        query += "email = %s, "
        params.append(email)

    query = query.rstrip(", ")

    query += " WHERE id = %s"
    params.append(ids)

    cursor.execute(query, tuple(params))


def deletenumber(cursor, idclient, phone):
    return cursor.execute("""delete from phone where idclient = %s and 
                             phone like %s""", (idclient, phone,))


def deleteclient(cursor, ids):
    cursor.execute("""select idclient from phone where idclient = %s""", (ids,))
    if cursor.fetchone() is not None:
        return print("Невозможно удалить клиента так как к нему привязан номер телефона")
    else:
        return cursor.execute("""delete from client where id = %s""", (ids,))


def findclient(cursor, name=None, surname=None, email=None, phone=None):
    query = """SELECT c.id, name, surname, email FROM client c
               LEFT JOIN phone p ON p.idclient = c.id
               WHERE 1=1"""
    params = []

    if name is not None:
        query += " AND name LIKE %s"
        params.append(f"%{name}%")
    if surname is not None:
        query += " AND surname LIKE %s"
        params.append(f"%{surname}%")
    if email is not None:
        query += " AND email LIKE %s"
        params.append(f"%{email}%")
    if phone is not None:
        query += " AND phone LIKE %s"
        params.append(f"%{phone}%")

    cursor.execute(query, tuple(params))
    return print(cursor.fetchall())


configcreateclient = """CREATE TABLE IF NOT EXISTS Client(
                  id SERIAL PRIMARY KEY,
                  name varchar(30) not null,
                  surname varchar(30) not null,
                  Email varchar(30) not null
                  );"""
configcreatephone = """CREATE TABLE IF NOT EXISTS Phone(
                    id SERIAL PRIMARY KEY,
                    phone varchar(15),
                    idclient integer references client(id)
                    );"""


if __name__ == "__main__":
    with psycopg2.connect(database="ClientsDB", user="postgres", password="") as con:
        with con.cursor() as cur:
            created_data_base(cur, configcreateclient)
            created_data_base(cur, configcreatephone)
            insertclient(cur, 'Михаил', 'Дремов', 'mixail_dremov@mail.ru')
            insertphone(cur, 1, '89850395812')
            updateclient(cur, 2, 'Антон', None, 'anton_m@mail.ru')
            deletenumber(cur, 1, '89850395812')
            deleteclient(cur, 1)
            insertclient(cur, 'Михаил', 'Дремов', 'mixail_dremov@mail.ru')
            insertphone(cur, 2, '89850395812')
            findclient(cur, None, None, "Дремов", None)
