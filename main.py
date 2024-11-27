import psycopg2


def created_data_base(cursor, config_create):
    return cursor.execute(config_create)


def insertclient(cursor, name, surname, email):
    return cursor.execute("""INSERT INTO Client (name, surname, Email)
                          values(%s, %s, %s);""", (name, surname, email,))


def insertphone(cursor, idclient, phone):
    return cursor.execute("""INSERT INTO Phone (idclient, phone)
                             values(%s ,%s)""", (idclient, phone,))


def updateclient(cursor, ids, name, surname, email):
    return cursor.execute("""UPDATE client SET name = %s, 
                             surname = %s, 
                             email = %s WHERE id = %s""", (name, surname, email, ids,))


def deletenumber(cursor, idclient, phone):
    return cursor.execute("""delete from phone where idclient = %s and 
                             phone like %s""", (idclient, phone,))


def deleteclient(cursor, ids):
    return cursor.execute("""delete from client where id = %s""", (ids,))


def findclient(cursor, name, surname, email, phone):
    cursor.execute("""select c.id, name, surname, email from client c
                             left join phone p on p.idclient = c.id
                             where name like %s and surname like %s and email like %s
                             or phone like %s""", (name, surname, email, phone,))
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


conn = psycopg2.connect(database="ClientsDB", user="postgres", password="")
with conn.cursor() as cur:
    created_data_base(cur, configcreateclient)
    created_data_base(cur, configcreatephone)
    insertclient(cur, 'Михаил', 'Дремов', 'mixail_dremov@mail.ru')
    insertphone(cur, 1, '89850395812')
    updateclient(cur, 1, 'Антон', 'Михайлов', 'anton_m@mail.ru')
    deletenumber(cur, 1, '89850395812')
    deleteclient(cur, 1)
    insertclient(cur, 'Михаил', 'Дремов', 'mixail_dremov@mail.ru')
    insertphone(cur, 2, '89850395812')
    conn.commit()
    findclient(cur, '%%', '%%', '%%', '89850395812')
conn.close()
