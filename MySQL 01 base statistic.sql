SELECT * FROM base.raw_data; -- Вся база даних
SELECT count(*) FROM base.raw_data; -- Кількість рядків в базі даних

SELECT count(*) FROM base.patients; -- Загальна кількість пацієнтів
-- 238 905 (31.12.23)
SELECT count(distinct pib, birthday) FROM patients; -- Загальна кількість пацієнтів
-- 238 835 (31.12.23)
SELECT SUM(t1.counter) FROM (SELECT COUNT(DISTINCT patient_order) AS counter FROM base.raw_data GROUP BY YEAR(date_order), MONTH(date_order)) AS t1; -- Кількість замовлень в базі даних
-- 460 120 (31.12.23)

SELECT COUNT(DISTINCT patient_order), SUM(cost_real) FROM base.raw_data WHERE date_order BETWEEN '2023-12-01' AND '2023-12-31'; -- Кількість замовлень в базі даних за грудень

-- Статистика по телефонам та email
SELECT count(*) FROM patients WHERE email IS not NULL; -- Кількість пацієнтів з email
SELECT count(distinct email) FROM patients WHERE email IS not NULL; -- Кількість пацієнтів з унікальними email
SELECT count(*) FROM patients WHERE email is null; -- Кількість пацієнтів без email
SELECT count(*) FROM patients WHERE phone <> ''; -- Кількість пацієнтів з номерами телефонів
SELECT count(*) FROM patients WHERE email IS not NULL AND phone <> ''; -- Кількість пацієнтів з email та телефоном
SELECT count(*) FROM patients WHERE email IS not NULL AND phone = ''; -- Кількість пацієнтів з email, але без телефона
SELECT count(*) FROM patients WHERE email IS NULL AND phone <> ''; -- Кількість пацієнтів без email, але телефоном 
SELECT count(*) FROM patients WHERE email IS NULL AND phone = ''; -- Кількість пацієнтів без телефону та email

-- Кількість нових пацієнтів (створених) у БД помісячно. Враховувалася дата першого замовлення.
SELECT YEAR(created_date) AS 'Рік', MONTH(created_date) AS 'Місяць', COUNT(*) AS 'Кількість' FROM patients GROUP BY YEAR(created_date), MONTH(created_date) ORDER BY YEAR(created_date), MONTH(created_date);
-- Групування пацієнтів по віку
SELECT count(id) AS 'Кількість', YEAR(CURDATE()) - YEAR(birthday) AS age FROM patients GROUP BY age ORDER BY age;
-- Групування пацієнтів по місяцю народження
SELECT MONTH(birthday) AS 'Місяць', COUNT(*) AS 'Кількість' FROM patients GROUP BY MONTH(birthday) ORDER BY MONTH(birthday);
-- Пацієнти з яким іменем який принесли доход
SELECT patients.fname, SUM(raw_data.cost_real) AS total_cost FROM patients JOIN raw_data ON patients.id = raw_data.patient_id GROUP BY patients.fname ORDER BY total_cost DESC;





-- Створення копії raw_data. Створюємо для перевірки гіпотез по оновленню бази даних
CREATE TABLE new_raw_data LIKE raw_data;
INSERT INTO new_raw_data SELECT * FROM raw_data;

SELECT *, concat(YEAR(date_order), '.', patient_order) AS order_number FROM base.raw_data;
SET SQL_SAFE_UPDATES = 0;
UPDATE raw_data SET raw_data.patient_order = concat(YEAR(date_order), '.', patient_order);

SELECT count(*) AS counter, patients.pib FROM raw_data INNER JOIN patients ON patients.id = raw_data.patient_id WHERE patients.tmp_valid_id is not null GROUP BY raw_data.patient_id ORDER BY counter DESC;
SELECT count(*) FROM patients WHERE tmp_valid_id IS not NULL;




CREATE TEMPORARY TABLE temp_result AS SELECT SUBSTRING_INDEX(p.email, ';', -1) AS femail, p.id, SUBSTRING_INDEX(p.email, ';', 1) AS semeil FROM patients AS p inner join blacklist_emails AS be ON be.email = SUBSTRING_INDEX(p.email, ';', -1) WHERE p.email LIKE '%;%';
DROP TEMPORARY TABLE temp_result;
SELECT * FROM temp_result;
SELECT LENGTH(email) - LENGTH(REPLACE(email, ';', '')) AS enamber, id FROM patients WHERE email LIKE '%;%' ORDER BY enamber DESC;
SELECT count(*) FROM patients WHERE email LIKE 'iqlab%' OR '%iqlab' OR '%iqlab%'; -- Для пошуку email iqlab

SELECT fname, count(fname) AS C1 FROM patients GROUP BY fname ORDER BY C1 DESC;
SELECT lname, count(lname) AS C1 FROM patients GROUP BY lname ORDER BY C1 DESC;
SELECT mname, count(mname) AS C1 FROM patients GROUP BY mname ORDER BY C1 DESC;
SET SQL_SAFE_UPDATES = 0; -- Виключення безпечного режиму перед оновленням та видаленням даних
UPDATE patients, temp_result 
SET patients.email = temp_result.semeil
WHERE patients.id = temp_result.id;
UPDATE patients
SET patients.email = null
WHERE patients.email = '';

-- Recency (R) — давність останньої покупки.
SELECT COUNT(*), DATE_FORMAT(dord, '%Y-%m') AS nm
FROM
    (SELECT patients.id, MAX(raw_data.date_order) AS dord
    FROM patients JOIN raw_data ON patients.id = raw_data.patient_id
    GROUP BY patients.id
    ORDER BY dord DESC) AS max_date
GROUP BY DATE_FORMAT(dord, '%Y-%m')
ORDER BY nm;

-- Recency (R) — давність останньої покупки з розділенням по типам офісів
CREATE TEMPORARY TABLE last_row SELECT MAX(rd.id) AS id FROM raw_data AS rd JOIN patients AS p ON p.id = rd.patient_id GROUP BY p.id;
CREATE INDEX idx_id ON last_row (id);
SELECT count(*), office_type, date_format(dord, '%Y-%m') AS nm FROM (SELECT last_row.id, o.office_type, rd.date_order AS dord FROM last_row
JOIN raw_data AS rd ON rd.id = last_row.id JOIN offices AS o ON o.id = rd.office_id GROUP BY rd.id, o.office_type) AS ss
GROUP BY date_format(dord, '%Y-%m'), office_type ORDER BY nm;

-- Frequency (F) — сумарна частота покупок за всю історію взаємодії з брендом.
SELECT count(*) AS orders, order_count FROM (SELECT count(*) AS order_count, patient_id FROM (SELECT patient_id, patient_order FROM raw_data GROUP BY patient_order, patient_id) AS f GROUP BY patient_id) AS t GROUP BY order_count ORDER BY order_count;
-- Вибрали пацієнтів по кількості замовленнь
SELECT p.*, order_count, patient_id FROM (SELECT count(*) AS order_count, patient_id FROM (SELECT patient_id, patient_order FROM raw_data GROUP BY patient_order, patient_id) AS f GROUP BY patient_id) AS t INNER JOIN patients AS p ON p.id = t.patient_id WHERE order_count >= 2 ORDER BY order_count;

SELECT 
    COUNT(*) AS orders, order_count, AVG(date_order)
FROM
    (SELECT 
        COUNT(*) AS order_count, patient_id, date_order
    FROM
        (SELECT 
        patient_id, patient_order, date_order
    FROM
        raw_data
    GROUP BY patient_order, patient_id, date_order) AS f
    GROUP BY patient_id, date_order) AS t
GROUP BY order_count
ORDER BY order_count;

SELECT patient_id, patient_order, MIN(date_order) AS md, DATEDIFF(MIN(date_order), '2018-12-06') AS days
    FROM raw_data
    GROUP BY patient_order, patient_id
    ORDER BY patient_id, md DESC;



-- Monetary (M)— загальна сума, витрачена на покупки
CREATE TABLE tmp_cost SELECT patient_id, SUM(cost_real) AS cr FROM raw_data GROUP BY patient_id;
SELECT count(*) FROM tmp_cost WHERE cr = '';
SELECT count(*) FROM tmp_cost WHERE cr < 30;
SELECT count(*) FROM tmp_cost WHERE cr >= 30 AND cr < 200;
SELECT count(*) FROM tmp_cost WHERE cr >= 200 AND cr < 400;
SELECT count(*) FROM tmp_cost WHERE cr >= 400 AND cr < 700;
SELECT count(*) FROM tmp_cost WHERE cr >= 700 AND cr < 1500;
SELECT count(*) FROM tmp_cost WHERE cr > 1500;

SELECT count(distinct patient_id) FROM (SELECT patient_id, patient_order, SUM(cost_return) FROM raw_data WHERE cost_return is not null GROUP BY patient_id, patient_order) AS r;
SELECT count(distinct patient_id) FROM (SELECT patient_id, cost_return FROM raw_data WHERE cost_return is not null) AS ret;

SELECT * FROM (SELECT patient_id, contract, SUM(cost_real) AS grn FROM raw_data WHERE date_order BETWEEN '2023-09-01 00:00:00' AND '2023-09-30 23:59:59' GROUP BY patient_id, contract) AS d GROUP BY contract;
-- Розподілення доходу по виду договору
SELECT contract, SUM(cost_real) AS grn FROM raw_data WHERE date_order BETWEEN '2023-11-01 00:00:00' AND '2023-11-30 23:59:59' GROUP BY contract;
