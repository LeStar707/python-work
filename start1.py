import pandas as pd

# Завантажуємо дані з Excel файлів
data = pd.read_excel('01-Paket.xlsx')  # Довідник
report = pd.read_excel('01-2023-03-copy.xlsx')  # Масив з даними
# Необхідно перевірити правильність наіменуваннь стовпчиків з даними 'Код Анализа', 'Ціна Факт'

results = {}

packages = {}


for test_id in report['Код Анализа'].items():

    if test_id in data['№ Тест IQLab'].items():












zvit = pd.DataFrame.from_dict(results, orient='index')
print(zvit)

