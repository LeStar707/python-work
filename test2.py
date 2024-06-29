import pandas as pd
import mysql.connector

# Підключення до MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="base"
)

cursor = mydb.cursor()


# Виконати запит і отримати результат
cursor.execute("SELECT m.*, offices.office, offices.city FROM(SELECT patients.id, patients.fname, patients.mname, patients.lname, patients.phone, raw_data.office_id, MAX(raw_data.date_order) AS MaxDR FROM raw_data INNER JOIN patients ON patients.id = raw_data.patient_id WHERE patients.phone IS not NULL AND patients.phone <> '' GROUP BY patients.id, raw_data.office_id) AS m INNER JOIN offices ON m.office_id = offices.id WHERE MaxDR <= '2019-06-30'")

# Отримати результат запиту
query_result = cursor.fetchall()

# Створити DataFrame з результатом запиту
df = pd.DataFrame(query_result, columns=['id', 'Ім"я', 'По-батькові', 'Прізвище', 'Телефон', 'id офісу','Дата останнього замовлення', 'Офіс', 'Місто'])

# Зберегти DataFrame у Excel
df.to_excel('result_export.xlsx', index=False)

