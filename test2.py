import pandas as pd

# Завантажуємо дані з Excel файлу
raw_report = pd.read_excel('2023_07.xlsx')  # Масив даних

# Функція, яка поєднує стовпчики Рік, Місяць, Число у новому стовпчику Дата
def compilation_date(day, month, year):
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    return str(day) + "." + str(months.index(month) + 1) + "." + str(year)


# Додаємо стовпець "Дата" з об'єднаними значеннями Рік, Місяць, Число
raw_report['Дата'] = raw_report.apply(lambda row: compilation_date(row['Число'], row['Місяць'], row['Рік']), axis=1)

# Створюємо новий DataFrame з потрібними стовпцями "Дата", "Виручка" та "Повернення"
income = raw_report[['Дата', 'Ціна Факт', 'Сума повернення']]

# Групуємо за датою і рахуємо суму замовлень та суму повернень коштів
income_sum = income.groupby('Дата').agg({'Ціна Факт': 'sum', 'Сума повернення': 'sum'}).reset_index()

# Дані у файлі сортуються по індексу (коду теста)
income_sum.to_excel('income.xlsx', index=False)
# Формує остаточний файл з даними у Excel

print(income_sum)

