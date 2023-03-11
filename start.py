import pandas as pd

# Завантажуємо дані з Excel файлу
data = pd.read_excel('Paket.xlsx')
report = pd.read_excel('2023-02-copy.xlsx')
# Виводимо перші 5 рядків даних
# print(data.head())
# print(report.head())
# print(report["Код Анализа"])

for paket_id in report["Код Анализа"]:

    if paket_id in data: #Шукае Код Аналіза у першому рядку
       print("Це пакет")
    else:
       for test_id in data["№ Тест IQLab"]: #Шукає Код Аналіза у першому стовпчику
            if test_id == paket_id:
                print("Це тест")
# А якщо Код Аналіза не знайдено?