

# Создайте файл crud_functions.py и напишите там следующие функции:

# initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса.
# Эта таблица должна содержать следующие поля:
#      id - целое число, первичный ключ
#      title(название продукта) - текст (не пустой)
#      description(описание) - текст
#      price(цена) - целое число (не пустой)

import sqlite3
connection = sqlite3.connect('product.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)    
    ''')

# get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.
def get_all_products():
    cursor.execute('SELECT  title, description, price FROM Products')
    products = cursor.fetchall()
    return products


initiate_db()

# Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.

for i in range(1, 5):
    cursor.execute("INSERT INTO Products(title, description, price) VALUES(?,?,?)",
                   (f'Продукт{i}', f'Описание{i}', f'{i*100}'))


connection.commit()
# connection.close()


