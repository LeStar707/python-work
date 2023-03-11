import pandas as pd

# Завантажуємо дані з Excel файлу
report = pd.read_excel('2023-02-copy.xlsx')

# Створюємо пустий DataFrame
# df = pd.DataFrame({'Код': [9029, 9034, 9040, 9080, 5014], 'Коментар': ['Пакет', 'Пакет','Пакет','Пакет','Тест']})
df = pd.DataFrame({'Код': report["Код Анализа"], 'Ціна Прайс': report["Ціна Прайс"], 'Ціна Факт': report["Ціна Факт"]})

# Виводимо DataFrame у файл Excel
df.to_excel('result.xlsx', index=False)