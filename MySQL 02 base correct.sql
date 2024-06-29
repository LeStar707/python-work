-- Запити для перевірки бази після завантаження нових даних
SELECT * FROM patients WHERE pib LIKE 'Забелин%'; -- Для пошуку тестових клієнтів Забелин
SELECT * FROM patients WHERE pib LIKE 'Тест%'; -- Для пошуку тестових клієнтів Тест
SELECT * FROM patients WHERE pib LIKE 'Контрол%'; -- Для пошуку тестових клієнтів Тест
SELECT * FROM patients WHERE pib REGEXP '^[0-9a-zA-Z\-]*$' AND email is null AND phone = ''; -- Пацієнти, у яких pib у вигляді коду та нема контактної інформації
SELECT * FROM patients WHERE pib REGEXP '[0-9]'; -- Для пошуку ПІБ пацієнтів, що мають у записі цифри
SELECT * FROM patients WHERE pib REGEXP '[a-zA-Z]'; -- Для пошуку ПІБ пацієнтів, що записані з використанням літер латиниці

SELECT * FROM patients WHERE email LIKE '%,%'; -- Для пошуку , у email
SELECT * FROM patients WHERE email LIKE '%@'; -- Для пошуку @ в кінці email
SELECT * FROM patients WHERE email LIKE '%;%' ORDER BY email; -- Для пошуку подвійних email
SELECT * FROM patients WHERE email LIKE '%bozhlazpsm@ukr.net%' ORDER BY email;
SELECT count(*) FROM patients WHERE email = ''; -- Кількість емейлів з пустою строкою

-- Зміна пустої строки у емейлі на null
SET SQL_SAFE_UPDATES = 0; -- Виключення безпечного режиму перед оновленням та видаленням даних
UPDATE patients SET patients.email = null WHERE patients.email = ''; -- Ставить null заміст пустої строки
-- Пошук повторних емейлів
SELECT email, count(email) FROM base.patients GROUP BY email; -- Емейл та кількість повторень
SELECT * FROM patients WHERE email = 'subba12081990@gmail.com'; -- Перелік пацієнтів з однаковими емейлами
UPDATE patients SET email = null WHERE email = 'subba12081990@gmail.com'; -- Ставить null заміст повторного емейла

-- Пошук дублів у БД по статі пацієнта (8)
SELECT count(*) AS counter, pib, birthday, group_concat(sex), group_concat(created_date) FROM patients GROUP BY pib, birthday having counter > 1 ORDER BY counter DESC;
-- Створення тимчасової таблиці зі знайдеми дублями
CREATE TEMPORARY TABLE tmp_dubbles SELECT count(*) AS counter, pib, birthday, group_concat(sex), group_concat(created_date) FROM patients GROUP BY pib, birthday having counter > 1 ORDER BY counter DESC;
-- Пошук повної інформації по задубльованим пацієнтам. Шукаємо співпадіння у таблиці пацієнтів з тимчасовою таблицею 
SELECT patients.* FROM patients INNER JOIN tmp_dubbles ON patients.pib = tmp_dubbles.pib AND patients.birthday = tmp_dubbles.birthday;
-- Виключення безпечного режиму перед оновленням та видаленням даних
SET SQL_SAFE_UPDATES = 0; -- Виключення безпечного режиму перед оновленням та видаленням даних
-- Сворюємо прив'язку між пацієнтами для заміни patient_id у raw_data
UPDATE patients SET tmp_valid_id = 38066 /*Видаляємо*/ WHERE `id` = 78399 /*Залишаємо*/;
-- Близнюки Горобець В.В., Нечай В.С., Пархоменко Д.С., Ралло В.І., Чепіга В.С.
-- Співпадіння - Дорошенко А.В., Корнієнко О.В., Шевченко В.М.
-- Заміна пацієнтів дублів у raw_data
UPDATE raw_data, patients SET raw_data.patient_id = patients.tmp_valid_id WHERE raw_data.patient_id = patients.id AND patients.tmp_valid_id is not null;
-- Видаляємо пацієнтів дублів у яких tmp_valid_id is not null
DELETE FROM patients WHERE tmp_valid_id is not null;