import os
import sys
import pandas as pd
import json
import glob
import math
import re
from datetime import datetime
import mysql.connector

# Підключення до MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="base"
)

# Створення курсора
cursor = connection.cursor()

# Виконання запиту для отримання числових даних з таблиці
query = "SELECT patient_id, patient_order, MIN(date_order) AS md, DATEDIFF(MIN(date_order), '2018-12-06') AS days FROM raw_data GROUP BY patient_order, patient_id ORDER BY patient_id, md DESC;"
cursor.execute(query)

# Отримання результатів запиту
results = cursor.fetchall()

# Закриття курсора та з'єднання
cursor.close()
connection.close()

patients = {}
# patient[1] = 35, patient[9] = 6
patient = {}

# Перетворення результатів у список чисел
for result in results:
    if result[0] in patient:
        if result[0] in patients:
            patients[result[0]].append(patient[result[0]] - result[3])
        else:
            patients[result[0]] = [patient[result[0]] - result[3]]
    patient[result[0]] = result[3]

df = pd.DataFrame(list(patients.items()), columns=['Patient ID', 'Values'])

# Розгортання списку в рядки
df = df.explode('Values')

# Експорт у файл Excel
df.to_excel('avg_orders_day.xlsx', index=False)
