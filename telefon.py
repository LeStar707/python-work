import re
import pandas as pd
# Коригування номерів телефонів у базі даних
raw_report = pd.read_excel('2023_03.xlsx')  # Масив даних


def normalize_phone_number(phone_number):
    # Видалення всіх непотрібних символів (лише цифри залишаються)
    if isinstance(phone_number, float):
        phone_number = str(phone_number)

    digits = re.sub(r'\D', '', phone_number)

    if digits != '':
        return '+380' + digits[-9:]
    else:
        return ''


phone_numbers = (raw_report['Номер телефону пацієнта'])

normalized_numbers = []
count_sum = 0

for number in phone_numbers:
    normalized_numbers.append(normalize_phone_number(number))
    if normalized_numbers[-1] != '':
        count_sum += 1

#print(normalized_numbers)

telefon = pd.DataFrame({'Скориговані номери': normalized_numbers})
telefon.to_excel('telefon.xlsx', index=False)

print('Кількість телефонних номерів: ', count_sum)

counts = {}
for length in range(8, 30):
    count = sum(len(number) == length for number in phone_numbers if isinstance(number, str))
    counts[length] = count
    print(f"{length} цифр - {count} номер.")

