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
       print("Це пакет: " + str(paket_id))
    else:
        if paket_id in data["№ Тест IQLab"].values: #Шукає Код Аналіза у першому стовпчику
            print("Це тест: " + str(paket_id))
        else:
            print('Тест не знайдений: ' + str(paket_id))

