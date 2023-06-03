import os
import pandas as pd
import json
from pymongo import MongoClient
import glob
import math

#raw_report = pd.read_excel('C:\\Python-project\\python-work\\mongodb\\2018_12_(20.05.23).xlsx')

folder_path = 'C:\\Python-project\\python-work\\mongodb'

# Отримуємо список всіх файлів у папці (включаючи підпапки)
file_list_from_os = glob.glob(folder_path + '/*.xlsx')

# З'єднання з MongoDB
#client = MongoClient('mongodb+srv://lestar707:EoEsaTrWGzXuWnF7@cluster0.tsytn6k.mongodb.net/?retryWrites=true&w=majority')
client = MongoClient('mongodb://localhost:27017')

# Вибір бази даних
db = client['Cluster0']

# Вибір колекції
collection = db['raw_report']


def parse_file_name(file_path):
    file_name_with_extension = os.path.basename(file_path)  # Парсимо весь шлях до файла. Залишаємо тільки назву файла та розширення
    file_name, file_extension = os.path.splitext(file_name_with_extension)  # Створюємо кортеж з назвою файлу та розшитенням
    return file_name


def modificate_clean_document(document: dict, file_path):
    del document['Місто']
    del document['Адреса']
    del document['Юридична назва']
    del document['Бренд']
    del document['Група послуги']
    del document['Виконавець тесту']
    del document['Форма Повернення']
    del document['Дисконт']
    del document['1']
    del document['Сума сплачено']
    del document['Сума продажу']
    del document['Знижка']
    file_name = parse_file_name(file_path)
    document.update({'file': file_name})
    return document


cursor = collection.aggregate([
    {
        '$group': {
            '_id': '$file',
        }
    },
    {
        '$sort': {
            '_id': 1
        }
    }
])

file_list_from_db = []

for file_name_from_db in cursor:
    file_list_from_db.append(file_name_from_db['_id'])


# Прочитати кожен файл у папці
for file_path_from_os in file_list_from_os:
    if parse_file_name(file_path_from_os) in file_list_from_db:
        continue

    raw_report = pd.read_excel(file_path_from_os)

    # Конвертувати DataFrame у список документів
    documents = json.loads(raw_report.to_json(orient='records'))

    bunch = []

    for document in documents:
        modify_document = modificate_clean_document(document, file_path_from_os)
        if modify_document['Код послуги'] is None or math.isnan(modify_document['Код послуги']):
            continue

        if len(bunch) < 10000:
            bunch.append(modify_document)
        else:
            bunch.append(modify_document)
            collection.insert_many(bunch)
            bunch = []

    if len(bunch) > 0:
        collection.insert_many(bunch)
        bunch = []

    #sys.exit(1) # Обробляємо тільки перший файл у папці

# Закриття з'єднання
client.close()

