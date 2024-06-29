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
cursor.execute("SELECT email, count(email) FROM base.patients GROUP BY email")

# Отримати результат запиту
query_result = cursor.fetchall()

# Створити DataFrame з результатом запиту
df = pd.DataFrame(query_result, columns=['email', 'count'])

# Зберегти DataFrame у Excel
df.to_excel('result_export.xlsx', index=False)