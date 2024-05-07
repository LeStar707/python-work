import mysql.connector
import pandas as pd
from tqdm import tqdm  # Імпорт бібліотеки tqdm для відображення прогресу
# Цей код додає нові електронні адреси до таблиці blacklist_emails, якщо вони відсутні у таблиці
# А також видаляє з таблиці patients електронні адреси, що потрапили у таблицю blacklist_emails
# При UPDATE таблиця blacklist_emails перевіряється повністю


# Підключення до бази даних
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="base"
)
cursor = mydb.cursor()

# Зчитування нових електронних адрес з файлу Excel
file_path = "emails.xlsx"  # Шлях до вашого файлу Excel
df = pd.read_excel(file_path)
new_emails = df["Email"].tolist()  # Адреси розміщені у стовпчику "Email"

# Додавання нових електронних адрес до таблиці blacklist_emails, якщо вони відсутні у таблиці
with tqdm(total=len(new_emails), desc="Оновлення blacklist_emails") as pbar:
    for email in new_emails:
        cursor.execute("SELECT COUNT(*) FROM blacklist_emails WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result[0] == 0:
            cursor.execute("INSERT INTO blacklist_emails (email) VALUES (%s)", (email,))
            mydb.commit()
        pbar.update(1)  # Оновлення прогрес-бара

# Видалення відповідних записів з таблиці patients, якщо вони є у списку blacklist_emails
with tqdm(total=len(new_emails), desc="Коригування емейлів у БД") as pbar:
    for email in new_emails:
        cursor.execute("SELECT COUNT(*) FROM blacklist_emails WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result[0] > 0:
            cursor.execute("UPDATE patients SET email = NULL WHERE email = %s", (email,))
            mydb.commit()
        pbar.update(1)  # Оновлення прогрес-бара

# Закриття з'єднання з базою даних
cursor.close()
mydb.close()
