import os
import pandas as pd
import json
import glob
import math
import re
from datetime import datetime
import mysql.connector

# Шлях до папки з файлами для завантаження
folder_path = 'C:\\Python-project\\python-work\\patient'

# Отримуємо список всіх файлів у папці (включаючи підпапки)
file_list_from_os = glob.glob(folder_path + '/*.xlsx')

# Підключення до MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="base"
)

# Функція, яка коригуе номери телефонів у формат +38 000 000 00 00
def normalize_phone_number(phone_number):
    if phone_number is None:
        return ''
    if isinstance(phone_number, float):
        phone_number = str(phone_number)
    digits = re.sub(r'\D', '', phone_number) # Видалення всіх непотрібних символів (лише цифри залишаються)
    if digits != '':
        return '+380' + digits[-9:]
    else:
        return ''


#Функція, яка змінює формат дати з 01.02.2000 на 2000.02.01
def format_date(date_object):
    date_object = datetime.strptime(date_object, "%d.%m.%Y")
    return date_object.strftime("%Y-%m-%d")


# Функція, яка поєднує стовпчики Рік, Місяць, Число у новому стовпчику Дата
def compilation_date(year, month, day):
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    return str(year) + "-" + str(months.index(month) + 1) + "-" + str(day)


# Функція, яка коригує стать пацієнта на m або f
def sex_patient(sex):
    if sex == 'Чол':
        sex = 'm'
    else:
        sex = 'f'
    return sex


# Функція, яка обєднує попередні функції та вносить коригування у базу даних
def modificate_clean_document(document: dict, file_path):
    date = compilation_date(document['Рік'], document['Місяць'], document['Число'])
    document.update({'Дата': date})

    document['Дата рождения пациента'] = format_date(document['Дата рождения пациента'])

    document['Стать'] = sex_patient(document['Стать'])

    document['Номер телефона пациента'] = normalize_phone_number(document['Номер телефона пациента'])

    return document


# Створюємо новий масив для запису назв файлів даних
file_list_from_db = []

cursor = mydb.cursor()

# Перевіряємо, які файли не завантажено до бази даних
for file_path_from_os in file_list_from_os:

    raw_report = pd.read_excel(file_path_from_os)

    # Конвертувати DataFrame у список документів
    documents = json.loads(raw_report.to_json(orient='records'))

    for document in documents:
        modify_document = modificate_clean_document(document, file_path_from_os)

        # Форматування даних для вставки у MySQL
        data = (document["Ім'я"], document['Прізвище'], document['По батькові'], document['Дата рождения пациента'],
                document['Номер телефона пациента'], document['E-mail Пациента'], document['Стать'],
                document['Пацієнт ПІБ'], document['Дата'])
        query = ("INSERT INTO patients (fname, lname, mname, birthday, phone, email, sex, pib, created_date) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) "
                 "ON DUPLICATE KEY UPDATE phone = VALUES(phone), email = VALUES(email)")
        cursor.execute(query, data)

    mydb.commit()

cursor.close()
mydb.close()

