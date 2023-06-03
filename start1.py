import math
import pandas as pd


def read_dictionary(file_path):
    return pd.read_excel(file_path)


def read_raw_report(file_path):
    return pd.read_excel(file_path)


def process_raw_report(dictionary, raw_report):
    results = {}
    packages = {}

    for report_string_id, package_id in raw_report["Код Анализа"].items():
        if package_id in dictionary:
            process_existing_package(package_id, report_string_id, dictionary, raw_report, results, packages)
        else:
            process_existing_test(package_id, report_string_id, dictionary, raw_report, results)

    calculate_package_costs(packages, results)
    return results


def process_existing_package(package_id, report_string_id, dictionary, raw_report, results, packages):
    if not math.isnan(raw_report.iloc[report_string_id]['Сумма Возврата']):
        package_cost = -raw_report.iloc[report_string_id]['Сумма Возврата']
    else:
        package_cost = raw_report.iloc[report_string_id]['Ціна Факт']

    packages.setdefault((package_id, report_string_id), {'package cost': package_cost})
    for dictionary_string_id, column_value in dictionary[package_id].items():
        if column_value == 1:
            test_id = dictionary.loc[dictionary_string_id]['№ Тест IQLab']
            results.setdefault(test_id, {'title': '', 'counter': 0, 'cost': 0})
            results[test_id]['counter'] += 1
            results[test_id]['title'] = dictionary.iloc[dictionary_string_id]['Тест IQ Lab']
            packages[(package_id, report_string_id)][test_id] = dictionary.iloc[dictionary_string_id]['Ціна']


def process_existing_test(package_id, report_string_id, dictionary, raw_report, results):
    if package_id in dictionary['№ Тест IQLab'].values:
        results.setdefault(package_id, {'counter': 0, 'cost': 0})
        results[package_id]['counter'] += 1
        dictionary_string_id_for_test = dictionary["№ Тест IQLab"].eq(package_id).idxmax()
        results[package_id]['title'] = dictionary.iloc[dictionary_string_id_for_test]['Тест IQ Lab']

        if not math.isnan(raw_report.iloc[report_string_id]['Ціна Факт']):
            results[package_id]['cost'] += raw_report.iloc[report_string_id]['Ціна Факт']
        else:
            print('Не вказана ціна :' + str(package_id))

        if not math.isnan(raw_report.iloc[report_string_id]['Сумма Возврата']):
            results[package_id]['counter'] -= 1
            results[package_id]['cost'] -= raw_report.iloc[report_string_id]['Сумма Возврата']
    else:
        print('Тест не знайдений: ' + str(package_id))


def calculate_package_costs(packages, results):
    for package_id_and_string_id, package_test_array in packages.items():
        package_cost = 0
        package_tests_cost_sum = 0

        for package_test_id, package_test_cost in package_test_array.items():
            if package_test_id == "package cost" and not math.isnan(package_test_cost):
                package_cost = package_test_cost
            elif not math.isnan(package_test_cost):
                if package_cost < 0:
                    results[package_test_id]['counter'] -= 1
                package_tests_cost_sum += float(package_test_cost)

        for package_test_id, package_test_cost in package_test_array.items():

            if package_test_id != "package cost" and not math.isnan(package_test_cost):
                test_percent = package_test_cost / package_tests_cost_sum
                test_new_cost = package_cost * test_percent
                results[package_test_id]['cost'] += float(test_new_cost)


if __name__ == "__main__":

    dictionary = read_dictionary('Paket.xlsx')
    raw_report = read_raw_report('2023-03.xlsx')
    results = process_raw_report(dictionary, raw_report)

    zvit = pd.DataFrame.from_dict(results, orient='index')
    # Формується словник у форматі pd.DataFrame з фінального масиву results
    zvit = zvit.sort_index()
    # Дані у файлі сортуються по індексу (коду теста)
    zvit.to_excel('zvit.xlsx', index=True)
    # Формує остаточний файл з даними у Excel
    print(zvit)
    # Виводить остаточний файл на екран


