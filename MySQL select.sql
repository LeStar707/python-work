SELECT * FROM base.raw_data; -- Вся база данихpatients
SELECT count(*) FROM base.raw_data; -- Кількість рядків в базі даних
SELECT SUM(t1.counter) FROM (SELECT COUNT(DISTINCT patient_order) AS counter FROM base.raw_data GROUP BY YEAR(date_order), MONTH(date_order)) AS t1; -- Кількість замовлень в базі даних
SELECT COUNT(DISTINCT patient_order) FROM base.raw_data WHERE date_order BETWEEN '2023-06-01' AND '2023-06-30'; -- Кількість замовлень в базі даних за червень
SELECT COUNT(DISTINCT patient, birthday) FROM base.raw_data; -- Кількість унікальних клієнтів в базі даних
SET SQL_SAFE_UPDATES = 0; -- Виключення безпечного режиму перед оновленням та видаленням даних
SELECT patient, birthday, COUNT(DISTINCT patient_order) AS order_count FROM base.raw_data GROUP BY patient, birthday; -- Формуємо список унікальних пацієнтів та визначаємо кількість замовлень у кожного пацієнта
SELECT * FROM base.raw_data WHERE office = 'Ваше здоров''я ПП';
SELECT COUNT(*) AS counter, t1.patient_order, group_concat(t1.Y), group_concat(t1.M) 
FROM (
	SELECT patient_order, YEAR(date_order) AS Y, MONTH(date_order) AS M 
	FROM base.raw_data 
	GROUP BY 
		YEAR(date_order),
		MONTH(date_order),
		patient_order
	ORDER BY 
		YEAR(date_order),
		MONTH(date_order)) AS t1 
GROUP BY 
    t1.patient_order 
ORDER BY counter DESC; -- Повтори номерів замовлень
SELECT 
    f1.office, COUNT(f1.patient)
FROM
    (SELECT 
        patient, birthday, office
    FROM
        base.raw_data
    /*WHERE date_order BETWEEN '2023-06-01' AND '2023-06-30'*/
    GROUP BY patient , birthday , office) AS f1
GROUP BY f1.office; -- Кількість пацієнтів по офісам
SELECT 
    f1.contract, COUNT(f1.patient)
FROM
    (SELECT 
        patient, birthday, contract
    FROM
        base.raw_data
	/*WHERE date_order BETWEEN '2023-06-01' AND '2023-06-30'*/
    GROUP BY patient, birthday, contract) AS f1
GROUP BY f1.contract; -- Кількість пацієнтів по договорам
SELECT 
    f1.company, COUNT(f1.patient)
FROM
    (SELECT 
        patient, birthday, company
    FROM
        base.raw_data
	/*WHERE date_order BETWEEN '2023-06-01' AND '2023-06-30'*/
    GROUP BY patient, birthday, company) AS f1
GROUP BY f1.company; -- Кількість пацієнтів по компаніям
SELECT cc.company, COUNT(cc.patient) FROM (SELECT patient, birthday, office, company FROM base.raw_data WHERE office = 'ТОВ "САНІТАС-Д"  IQLAB Відділення №101, м. Дніпро, пр. Героїв, 22а' AND company <> 'Фізична особа' GROUP BY patient, birthday, company) AS cc GROUP BY cc.company; -- Кількість КК оформлених у Віддіденні №101
SELECT cc.company, COUNT(cc.patient) FROM (SELECT patient, birthday, office, company FROM base.raw_data WHERE office = 'ТОВ "САНІТАС-Д"  IQLAB Відділення №102, м. Дніпро, пр. Миру, 55/5' AND company <> 'Фізична особа' GROUP BY patient, birthday, company) AS cc GROUP BY cc.company; -- Кількість КК оформлених у Віддіденні №102
SELECT t1.office, t1.company, count(t1.patient) FROM(SELECT patient, birthday, office, company FROM base.raw_data GROUP BY patient, birthday, office, company) AS t1 GROUP BY t1.office, t1.company; -- Співвідношення office та company

