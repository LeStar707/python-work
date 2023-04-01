import pandas as pd

# Завантажуємо дані з Excel файлу
data = pd.read_excel('Paket.xlsx')
report = pd.read_excel('2023-02-copy.xlsx')

results = {}

# {
# 1054: {count: 156, cost: 5690.56},
# 1055: {count: 15, cost: 1600.6},
# }

packages = {}

# {
# (9080, 3): {'package cost': 1000.50, 1054: 50.98, 1055: 200.35}
# (9080, 13): {'package cost': 950.50, 1054: 50.98, 1055: 200.35}
# (9081, 14): {'package cost': 600, 1054: 50.98, 1056: 160.0}
# }

for report_num, paket_id in report["Код Анализа"].items():  # Код пакету чи код аналізу

    if paket_id in data:  # Шукае код пакету у першому рядку
        packages.setdefault((paket_id, report_num), {'package cost': report.iloc[report_num]['Ціна Факт']})

        for key, val in data[paket_id].items():  # Отримуємо ключ та значення з стовпчика з кодом пакета

            if val == 1:  # Шукаємо значення 1 у стовпчику пакета та відбираємо коди тестів що в нього входять
                test_id = data.loc[key]['№ Тест IQLab']
                results.setdefault(test_id, {'counter': 0, 'cost': 0})
                results[test_id]['counter'] += 1
                # packages[(paket_id, report_num)][test_id] = data.iloc[key]['Ціна']

    else:  # Пошук окремих тестів
        if paket_id in data["№ Тест IQLab"].values:  # Шукає код тесту у першому стовпчику
            results.setdefault(paket_id, {'counter': 0, 'cost': 0})
            results[paket_id]['counter'] += 1
            results[paket_id]['cost'] += report.iloc[report_num]['Ціна Факт']
        else:
            print('Тест не знайдений: ' + str(paket_id))

for package_key, package_value in packages.items():
    package_cost = 0
    tests_sum = 0
    for test_key, test_cost in package_value.items():
        if test_key == "package cost":
            package_cost = test_cost
        else:
            tests_sum += test_cost

    for test_key, test_cost in package_value.items():
        if test_key != "package cost":
            test_percent = test_cost / tests_sum
            test_new_cost = package_cost * test_percent
            results[test_key]['cost'] += test_new_cost


# zvit = pd.DataFrame(list(results.items()), columns=['Код', 'Кількість', 'Сума'])
# zvit.to_excel('zvit.xlsx', index=False)
print(results)

