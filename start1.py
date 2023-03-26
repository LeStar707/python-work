import pandas as pd

# Завантажуємо дані з Excel файлів
price = pd.read_excel('price.xlsx')
paket = pd.read_excel('paket1.xlsx')
report = pd.read_excel('2023-02-copy.xlsx')

# Створюємо словник для зберігання результатів запросу
results = {}

# Рахуємо одинокі тести з бази даних
for test_id in report["Код Анализа"]:

    if test_id in price["№ Тест IQLab"].values:  # Шукае Код Аналіза у прайсі
         if test_id in results:
             results[test_id] += 1
         else:
             results[test_id] = 1

print(results)

zvit = pd.DataFrame(list(results.items()), columns=['Код', 'Кількість'])

zvit.to_excel('result.xlsx', index=False)

print(zvit)




