import os
import sys
import pandas as pd
import json
import glob
import math
import re
from datetime import datetime
import mysql.connector

# raw_report = pd.read_excel('C:\\Python-project\\python-work\\mysql\\2018_12_(20.05.23).xlsx')

# Шлях до папки з файлами для завантаження
folder_path = 'C:\\Python-project\\python-work\\mysql'

# Отримуємо список всіх файлів у папці (включаючи підпапки)
file_list_from_os = glob.glob(folder_path + '/*.xlsx')

# Підключення до MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="base"
)

cursor = mydb.cursor()

# Функція, яка видаляе зайві стовпчики даних
def removing_columns():
    del document['Місяць']
    del document['Число']
    del document['Рік']


# Функція, яка прибирає повну адресу до файлу імпорту та розширення, залишаючи тільки його назву
def parse_file_name(file_path):
    # Парсимо весь шлях до файла. Залишаємо тільки назву файла та розширення
    file_name_with_extension = os.path.basename(file_path)
    # Створюємо кортеж з назвою файлу та розширенням
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    return file_name


# Функція, яка отримує всі назви завантажених файлів з MySQL з таблиці raw_data.file
def get_file_names_from_db():
    query = ("SELECT file FROM raw_data GROUP BY file")
    cursor.execute(query)
    return [file[0] for file in cursor.fetchall()]


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
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    return str(year) + "-" + str(months.index(month) + 1) + "-" + str(day)


# Функція, яка коригує стать пацієнта на m або f
def sex_patient(sex):
    if sex == 'Чол':
        sex = 'm'
    else:
        sex = 'f'
    return sex


# Функція, яка коригує пробіли та коми у email
def correct_email_format(email):
    # Видаляємо всі пробіли
    if email is None:
        return email
    email = re.sub(r'\s', '', email)
    # Питаємо у користувача, на який символ скоригувати email
    if "," in email:
        print("Знайдений знак ',' у полі email:", email)
        choice = input("Введіть 1, щоб замінити на '.' або 2, щоб замінити на ';': ")
        if choice == "1":
            email = re.sub(r',', '.', email)
        elif choice == "2":
            email = re.sub(r',', ';', email)
        else:
            print("Некоректний вибір. Залишаю значення без змін.")
    return email


# Функція яка аналізує подвійні email-адреси та видаляє email, що занасені до blacklist_emails
def check_blacklist_emails(email):
    if email is None:
        return email
    if ";" in email:
        # Розділення email на частини за допомогою символу ";"
        parts = email.split(";")
        # Перевірка першої частини email
        if remove_bad_emails(parts[0].strip()) is not None:
            parts[0] = ""
        # Перевірка другої частини email
        if remove_bad_emails(parts[1].strip()) is not None:
            parts[1] = ""
        email = ";".join(parts)
    else:
        if remove_bad_emails(email) is not None:
            return ""
        else:
            return email
    return email


# Функція  видаляє email, що занасені до blacklist_emails
# 123@gmail.com - None
# iqlab@example.com - not None
def remove_bad_emails(email):
    sql = 'SELECT email, %s REGEXP email AS is_blacklisted FROM blacklist_emails HAVING is_blacklisted = 1 LIMIT 1'
    cursor.execute(sql, (email,))
    return cursor.fetchone()


# Функція, яка додає дані про нових пацієнтів у базу даних у таблицю patients
def add_patient_to_db(document):
    sql = 'SELECT id, phone, email FROM patients WHERE pib = %s AND birthday = %s AND sex = %s LIMIT 1'
    cursor.execute(sql, (document['Пацієнт'], document['Дата народження пацієнта'], document['Стать пацієнта']))
    result = cursor.fetchone()
    email = correct_email_format(document['E-mail пацієнта'])
    email = check_blacklist_emails(email)
    if result is not None:
        if result[1] != document['Номер телефону пацієнта'] or result[2] != email:
            sql = 'UPDATE patients SET phone = %s, email = %s WHERE id = %s'
            cursor.execute(sql, (document['Номер телефону пацієнта'], email, result[0]))
        return result[0]

    data = (document["Ім'я"], document['Прізвище'], document['По батькові'], document['Дата народження пацієнта'],
            document['Номер телефону пацієнта'], email, document['Стать пацієнта'],
            document['Пацієнт'], document['Дата'])
    query = ("INSERT INTO patients (fname, lname, mname, birthday, phone, email, sex, pib, created_date) "
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(query, data)
    # Отримати ідентифікатор нового пацієнта
    return cursor.lastrowid


def add_office_to_db(document):
    sql = 'SELECT office_id FROM offices_rel WHERE original_name = %s LIMIT 1'
    if document['Замовлення послуг. Контрагент'] == 'Фізична особа':
        office_name = (document['Медичний офіс'],)
    else:
        office_name = (document['Замовлення послуг. Контрагент'],)

    if office_name[0] is None:
        office_name = ('ТОВ "САНІТАС-Д"  IQLAB Відділення №101, м. Дніпро, пр. Героїв, 22а',)

    cursor.execute(sql, office_name)
    result = cursor.fetchone()
    if result is not None:
        return result[0]

    query = "INSERT INTO offices_rel (original_name) VALUES (%s)"
    cursor.execute(query, office_name)
    print('Додали нову компанію: ' + office_name[0])
    sys.exit()


# Функція, яка обєднує попередні функції та вносить коригування у базу даних
def modificate_clean_document(document: dict, file_path):
    date = compilation_date(document['Рік'], document['Місяць'], document['Число'])
    document.update({'Дата': date})

    document['Дата народження пацієнта'] = format_date(document['Дата народження пацієнта'])

    document['Стать пацієнта'] = sex_patient(document['Стать пацієнта'])

    document['Номер телефону пацієнта'] = normalize_phone_number(document['Номер телефону пацієнта'])

    file_name = parse_file_name(file_path)
    document.update({'file': file_name})

    return document

# Створюємо новий масив для запису назв файлів даних
file_list_from_db = get_file_names_from_db()


# Перевіряємо, які файли не завантажено до бази даних
for file_path_from_os in file_list_from_os:
    if parse_file_name(file_path_from_os) in file_list_from_db:
        continue

    raw_report = pd.read_excel(file_path_from_os)

    # Конвертувати DataFrame у список документів
    documents = json.loads(raw_report.to_json(orient='records'))

    # Перевіряємо існування офісів
    for document in documents:
        add_office_to_db(document)

    # Проходження по документам
    for document in documents:
        # Модифікація документа
        modify_document = modificate_clean_document(document, file_path_from_os)
        # Додавання пацієнта до бази даних
        patient_id = add_patient_to_db(modify_document)
        # Додавання офісу до бази даних
        office_id = add_office_to_db(modify_document)
        # Видалення непотрібних стовпців
        removing_columns()  # Записуємо останнім, оскільки видаляємо стовпці, які використовуються в інших функціях
        # Пропуск ітерації, якщо 'Код послуги' є None або NaN
        if modify_document['Код послуги'] is None or math.isnan(modify_document['Код послуги']):
            continue

        # Підготовка даних для вставки
        data = (document['Лікар'],
                document['Спеціалізація лікаря'], document['ЛПЗ'],
                document['Назва послуги'], document['Код послуги'], document['Форма платежу'],
                document['Договір / Акція'], document['Номер замовлення'], document['Код купона'],
                document['Ціна Прайс'], document['Ціна Факт'], document['Сума повернення'], document['Дата'],
                document['file'], patient_id, office_id)
        # Виконання SQL-запиту для вставки даних в таблицю raw_data
        query = ("INSERT INTO raw_data (doctor, doctor_specialisation, hospital, service_name, service_code, "
                 "payment_type, contract, patient_order, promo_code, cost_price, cost_real, cost_return, date_order, "
                 "file, patient_id, office_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(query, data)

    mydb.commit()

cursor.close()
mydb.close()

