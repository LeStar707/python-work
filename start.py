import math

import pandas as pd

# Завантажуємо дані з Excel файлу
data = pd.read_excel('Paket.xlsx')
report = pd.read_excel('2023-02-copy.xlsx')

results = {}
# Створюємо масив виду
# {
# 4024: {'title': "Білок", 'counter': 246, 'cost': 9859.210000000001},
# 4025: {'title': "Сечовина", 'counter': 355, 'cost': 21265.23},
# }

packages = {}
# Створюємо масив виду
# {
# (9080, 1): {'package cost': 265.50, 4024: 88.50, 4025: 88.50, 4026: 88.50}
# (9040, 18): {'package cost': 530.00, 9026: 205.87, 5014: 162.07, 9009: 162.07}
# (9080, 62): {'package cost': 265.50, 4024: 88.50, 4025: 88.50, 4026: 88.50}
# }

for report_num, paket_id in report["Код Анализа"].items():  # Визначаємо Код пакету чи Код аналізу

    if paket_id in data:  # Шукае код пакету у першому рядку
        packages.setdefault((paket_id, report_num), {'package cost': report.iloc[report_num]['Ціна Факт']})

        for key, val in data[paket_id].items():  # Отримуємо ключ та значення з стовпчика з кодом пакета

            if val == 1:  # Шукаємо значення 1 у стовпчику пакета та відбираємо коди тестів що в нього входять
                test_id = data.loc[key]['№ Тест IQLab']
                results.setdefault(test_id, {'title': '', 'counter': 0, 'cost': 0})
                results[test_id]['counter'] += 1
                results[test_id]['title'] = data.iloc[key]['Тест IQ Lab']
                packages[(paket_id, report_num)][test_id] = data.iloc[key]['Ціна']


    else:  # Пошук окремих тестів
        if paket_id in data["№ Тест IQLab"].values:  # Шукає код тесту у першому стовпчику
            results.setdefault(paket_id, {'counter': 0, 'cost': 0})
            results[paket_id]['counter'] += 1
            test_column_number = data["№ Тест IQLab"].index[data["№ Тест IQLab"].eq(paket_id)].tolist()[0]
            results[paket_id]['title'] = data.iloc[test_column_number]['Тест IQ Lab']
            if not math.isnan(report.iloc[report_num]['Ціна Факт']):
                results[paket_id]['cost'] += report.iloc[report_num]['Ціна Факт']
            else:
                print('Не вказана ціна :' + str(paket_id))
        else:
            print('Тест не знайдений: ' + str(paket_id))

for package_key, package_value in packages.items():
    package_cost = 0
    tests_sum = 0
    for test_key, test_cost in package_value.items():
        if test_key == "package cost" and not math.isnan(test_cost):
            package_cost = test_cost
        elif not math.isnan(test_cost):
            tests_sum += float(test_cost)

    for test_key, test_cost in package_value.items():
        if test_key != "package cost" and not math.isnan(test_cost):
            test_percent = test_cost / tests_sum
            test_new_cost = package_cost * test_percent
            results[test_key]['cost'] += float(test_new_cost)

zvit = pd.DataFrame.from_dict(results, orient='index')
zvit.to_excel('zvit.xlsx', index=True)
print(zvit)

