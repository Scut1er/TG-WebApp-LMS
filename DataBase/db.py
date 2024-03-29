import sqlite3

connection = sqlite3.connect('DataBase/lms.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
tg_id INTEGER PRIMARY KEY,
fio TEXT DEFAULT "Пользователь" NOT NULL,
email TEXT)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Tickets (
id INTEGER PRIMARY KEY AUTOINCREMENT,
tg_id INTEGER,
message TEXT NOT NULL)
''')


def get_user_db(tg_id):
    user = cursor.execute('''SELECT * FROM Users WHERE tg_id=?''', (tg_id,)).fetchone()
    return user


def add_user_db(tg_id, fio, email):  # Добавление в базу нового пользователя
    cursor.execute('''INSERT INTO Users (tg_id, fio, email)
     SELECT ?, ?, ? WHERE NOT EXISTS (SELECT * FROM Users WHERE tg_id = ?)''', (tg_id, fio, email, tg_id))
    connection.commit()


def add_ticket_db(tg_id, message):  # Добавление в базу нового пользователя
    cursor.execute('''INSERT INTO Tickets (tg_id, message)
     SELECT ?, ?''', (tg_id, message))
    connection.commit()


def update_email_db(tg_id, email):
    cursor.execute('''UPDATE Users SET email = ? WHERE tg_id=?''', (email, tg_id))
    connection.commit()
