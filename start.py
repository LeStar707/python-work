import pandas as pd

# Завантажуємо дані з Excel файлу
data = pd.read_excel('Paket.xlsx')
report = pd.read_excel('2023-02-copy.xlsx')
# Виводимо перші 5 рядків даних
# print(data.head())
# print(report.head())
# print(report["Код Анализа"])
results = {}

for paket_id in report["Код Анализа"]:  # Код пакету чи код аналізу

    if paket_id in data:  # Шукае код пакету у першому рядку

        for key, val in data[paket_id].items():  # Отримуємо ключ та значення з стовпчика з номером пакета

            if val == 1:  # Шукаємо значення 1, що в пакеті є такий тест
                test_id = data.loc[key]['№ Тест IQLab']
                results.setdefault(test_id, 0)
                results[test_id] += 1

    else:  # Пошук окремих тестів
        if paket_id in data["№ Тест IQLab"].values:  # Шукає код тесту у першому стовпчику
            results.setdefault(paket_id, 0)
            results[paket_id] += 1

        else:
            print('Тест не знайдений: ' + str(paket_id))

zvit = pd.DataFrame(list(results.items()), columns=['Код', 'Кількість'])
zvit.to_excel('zvit.xlsx', index=False)
print(results)
