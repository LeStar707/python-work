import math
import pandas as pd
from datetime import datetime

# Завантажуємо дані з Excel файлу
dictionary = pd.read_excel('Paket.xlsx')  # Довідник
raw_report = pd.read_excel('2023_08.xlsx')  # Масив даних
# Необхідно перевірити правильність наіменуваннь стовпчиків з даними 'Код послуги', 'Ціна Факт'

# Функція, яка поєднує стовпчики Рік, Місяць, Число у новому стовпчику Дата
def compilation_date(day, month, year):
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    input_date = str(day) + "." + str(months.index(month) + 1) + "." + str(year)
    # Форматуємо текст у дату
    parsed_date = datetime.strptime(input_date, "%d.%m.%Y")
    # Форматування дати у рядок з допомогою методу strftime()
    return parsed_date.strftime("%d.%m.%Y")


results = {}
''' Створюємо масив виду
{
4024: {'title': "Сечовина", 'counter': 246, 'cost': 9859.210000000001},
4025: {'title': "Сечова кислота", 'counter': 355, 'cost': 21265.23},
}
'''
packages = {}
'''Створюємо масив виду
{
(9080, 1): {'package cost': 265.50, 4024: 88.50, 4025: 88.50, 4026: 88.50}
(9040, 18): {'package cost': 530.00, 9026: 205.87, 5014: 162.07, 9009: 162.07}
(9080, 62): {'package cost': 265.50, 4024: 88.50, 4025: 88.50, 4026: 88.50}
}
'''
for report_string_id, package_id in raw_report["Код послуги"].items():
# Вибираємо номер строки і Код пакету / Код аналізу у значеннях стовпчика 'Код послуги' у Масиві даних

    if package_id in dictionary:
    # Шукае Код пакету у першому рядку Довідника
        if not math.isnan(raw_report.iloc[report_string_id]['Сума повернення']):
            # Якщо є сума повернення, то зберігаємо її у змінну package_cost зі знаком "-"
            package_cost = -raw_report.iloc[report_string_id]['Сума повернення']
        else:
            # Якщо немає суми повернення, то беремо фактичну ціну
            package_cost = raw_report.iloc[report_string_id]['Ціна Факт']

        packages.setdefault((package_id, report_string_id), {'package cost': package_cost})
        # Встановлюємо дані за замовченням для масиву packages
        # Сворюємо подвійний ключ (кортеж (package_id, report_string_id)) та значення для ключа у вигляді масиву, який має
        # один ключ "package cost", що містить значення з рядка report_num та стовпця "Ціна Факт" з Масиву даних

        for dictionary_string_id, column_value in dictionary[package_id].items():
        # Визначаємо які тести входять у пакет
        # Отримуємо ключ та значення із Довідника зі стовпчика з кодом пакета
            if column_value == 1:
            # Шукаємо значення 1 у стовпчику з кодом пакета

                test_id = dictionary.loc[dictionary_string_id]['№ Тест IQLab']
                # При знаходженні 1, передаємо код тесту у змінну test_id з Довідника

                results.setdefault(test_id, {'title': '', 'counter': 0, 'cost': 0})
                # Встановлюємо дані за замовченням для масиву results
                # Ключем для масиву буде код тесту test_id, а значенням - масив з наступними даними
                # Назва тесту 'title' - пуста строка
                # Кількість проданих тестів 'counter' = 0
                # Загальна сума продажу по тесту 'cost' = 0

                results[test_id]['counter'] += 1
                # При знаходженні 1, збільшуємо кількість проданих тестів 'counter' на 1 для відповідного тесту

                results[test_id]['title'] = dictionary.iloc[dictionary_string_id]['Тест IQ Lab']
                # При знаходженні 1, переносимо назву тесту у стовпчик 'title' з Довідника

                packages[(package_id, report_string_id)][test_id] = dictionary.iloc[dictionary_string_id]['Ціна']
                # При знаходженні 1, наповнюємо масив packages даними про роздрібну ціну тесту з Довідника

    else:
    # Якщо код пакету не знайдено у першому рядку Довідника, то це тест

        if package_id in dictionary['№ Тест IQLab'].values:
        # Шукає код тесту у стовпчику '№ Тест IQLab' у Довіднику

            results.setdefault(package_id, {'counter': 0, 'cost': 0})
            # Встановлюємо дані за замовченням для масиву results

            results[package_id]['counter'] += 1
            # Збільшуємо кількість проданих тестів 'counter' на 1 для відповідного тесту

            dictionary_string_id_for_test = dictionary["№ Тест IQLab"].eq(package_id).idxmax()
            # Отримуємо номер строки у Довіднику який співпадає з package_id

            results[package_id]['title'] = dictionary.iloc[dictionary_string_id_for_test]['Тест IQ Lab']
            # Отримуємо назву тесту з Довідника

            if not math.isnan(raw_report.iloc[report_string_id]['Ціна Факт']):
                # Якщо у Масиві даних 'Ціна Факт' не пуста
                results[package_id]['cost'] += raw_report.iloc[report_string_id]['Ціна Факт']
                # Додаємо 'Ціна Факт' до загальної суми
            else:
                print('Не вказана ціна :' + str(package_id))
                # Виводить на екран прелік тестів, по яким не вказана 'Ціна Факт'
                # Скорше за все - це повернення коштів

            if not math.isnan(raw_report.iloc[report_string_id]['Сума повернення']):
                # Якщо 'Сума повернення' не пуста
                results[package_id]['counter'] -= 1
                # Віднімаємо тест від уже порахованої кількості
                results[package_id]['cost'] -= raw_report.iloc[report_string_id]['Сума повернення']
                # Віднімаємо суму повернення по тесту від уже порахованої суми
        else:
            print('Тест не знайдений: ' + str(package_id))
            # Виводить номер тесту, який не знайдений у Довіднику

for package_id_and_string_id, package_test_array in packages.items():
    # Отримуємо елементи з масиву packages
    # package_id_and_string_id = (9080, 1)
    # package_test_array = {'package cost': 265.50, 4024: 88.50, 4025: 88.50, 4026: 88.50}
    package_cost = 0
    package_tests_cost_sum = 0
    # Встановили значення за замовченням

    # Підраховуємо всю суму тестів у пакеті
    for package_test_id, package_test_cost in package_test_array.items():
        # Отримали номер та ціну тесту з масиву package_test_array
        # package_test_id = 'package cost' / 4024 / 4025 / 4026
        # package_test_cost = 265.50 / 88.50 / 88.50 / 88.50
        if package_test_id == "package cost" and not math.isnan(package_test_cost):
            # Якщо package_test_id = "package cost" і ціна пакету не 0
            package_cost = package_test_cost
            # Зберігаємо у зміну package_cost
        elif not math.isnan(package_test_cost):
            # Обробляємо тести з пакету
            if package_cost < 0:
                # Якщо сума пакет < 0 ми розуміємо, що це повернення і віднімаємо 1 від кількості тестів
                results[package_test_id]['counter'] -= 1
            # Якщо ціна пакету не 0
            package_tests_cost_sum += float(package_test_cost)
            # У загальну суму тестів додаємо суму тесту

    # У цьому циклі підраховуємо долю кожного тесту в пакеті
    for package_test_id, package_test_cost in package_test_array.items():
        # Отримали номер та ціну тесту з масиву package_test_array
        # package_test_id = 'package cost' / 4024 / 4025 / 4026
        # package_test_cost = 265.50 / 110.0 / 110.0 / 110.0
        if package_test_id != "package cost" and not math.isnan(package_test_cost):
            # Вартість пакету не враховуємо, працюємо тільки з тестами
            test_percent = package_test_cost / package_tests_cost_sum
            # Беремо ціну одного тесту у пакеті і ділимо на суму всих тестів у цьому пакеті = 110.0 / 330.0 = 0.333
            test_new_cost = package_cost * test_percent
            # 265.50 * 0.333
            results[package_test_id]['cost'] += float(test_new_cost)
            # Додаємо до масиву results у стовпчик ціни тесту результат обчислення вартості тесту у пакеті

# Формується словник у форматі pd.DataFrame з фінального масиву results
zvit = pd.DataFrame.from_dict(results, orient='index')
# Дані у файлі сортуються по індексу (коду теста)
zvit = zvit.sort_index()
# Формує остаточний файл з даними у Excel
zvit.to_excel('zvit.xlsx', index=True)
# Виводить остаточний файл на екран
print(zvit)

# Формуємо окремий файл з сумами виручки та повернень коштів за кожен день

# Додаємо стовпець "Дата" з об'єднаними значеннями Рік, Місяць, Число
raw_report['Дата'] = raw_report.apply(lambda row: compilation_date(row['Число'], row['Місяць'], row['Рік']), axis=1)
# Створюємо новий DataFrame з потрібними стовпцями "Дата", "Виручка" та "Повернення"
income = raw_report[['Дата', 'Ціна Факт', 'Сума повернення']]
# Групуємо за датою і рахуємо суму замовлень та суму повернень коштів
income_sum = income.groupby('Дата').agg({'Ціна Факт': 'sum', 'Сума повернення': 'sum'}).reset_index()
# Формує остаточний файл з даними у Excel
income_sum.to_excel('income.xlsx', index=False)

print(income_sum)
