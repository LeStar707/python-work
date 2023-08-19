import os
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

# Функція, яка видаляе зайві стовпчики даних
def removing_columns():
    del document['Тиждень']
    del document['День тижня']
    del document['Адреса']
    del document['Юридична назва']
    del document['КК']
    del document['Бренд']
    del document['Вік пацієнта']
    del document['Група послуги']
    del document['Виконавець тесту']
    del document['Форма Повернення']
    del document['Направлення лікаря']
    del document['Ваучер']
    del document['Дисконт']
    del document['1']
    del document['Сума сплачено']
    del document['Сума продажу']
    del document['Знижка']
    del document['Повернення']
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

    document['Дата народження пацієнта'] = format_date(document['Дата народження пацієнта'])

    document['Стать пацієнта'] = sex_patient(document['Стать пацієнта'])

    document['Номер телефону пацієнта'] = normalize_phone_number(document['Номер телефону пацієнта'])

    file_name = parse_file_name(file_path)
    document.update({'file': file_name})

    removing_columns()  # Записуємо останнім, бо видаляємо стовпчики які використовували в інших функціях
    return document

# Створюємо новий масив для запису назв файлів даних
file_list_from_db = []

# Записуємо назви файлів даних у масив
# for file_name_from_db in cursor:
#     file_list_from_db.append(file_name_from_db['_id'])

cursor = mydb.cursor()

# Перевіряємо, які файли не завантажено до бази даних
for file_path_from_os in file_list_from_os:
    if parse_file_name(file_path_from_os) in file_list_from_db:
        continue

    raw_report = pd.read_excel(file_path_from_os)

    # Конвертувати DataFrame у список документів
    documents = json.loads(raw_report.to_json(orient='records'))

    for document in documents:
        modify_document = modificate_clean_document(document, file_path_from_os)
        if modify_document['Код послуги'] is None or math.isnan(modify_document['Код послуги']):
            continue

        # Форматування даних для вставки у MySQL
        data = (document['Медичний офіс'], document['Менеджер'], document['Пацієнт'], document['Стать пацієнта'], document['Дата народження пацієнта'], document['Номер телефону пацієнта'], document['Лікар'], document['Спеціалізація лікаря'], document['Відсоток лікаря %'], document['ЛПЗ'], document['Назва послуги'], document['Код послуги'], document['Форма оплати'], document['Договір / Акція'], document['Номер замовлення'], document['Код купона'], document['E-mail пацієнта'], document['Замовлення послуг. Контрагент'], document['Ціна Прайс'], document['Ціна Факт'], document['Сума повернення'], document['Дата'], document['file'])
        query = "INSERT INTO raw_data (office, manager, patient, sex, birthday, phone, doctor, doctor_specialisation, doctor_rate, hospital, service_name, service_code, payment_type, contract, patient_order, promo_code, email, company, cost_price, cost_real, cost_return, date_order, file) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, data)

        # if len(bunch) < 10000:
        #     bunch.append(modify_document)
        # else:
        #     bunch.append(modify_document)
        #     collection.insert_many(bunch)
        #     bunch = []

    mydb.commit()

    # if len(bunch) > 0:
    #     collection.insert_many(bunch)
    #     bunch = []

cursor.close()
mydb.close()

