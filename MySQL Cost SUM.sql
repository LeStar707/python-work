SELECT SUM(cost_real) FROM base.raw_data WHERE date_order BETWEEN '2023-06-01' AND '2023-06-30'; -- Доход за червень
SELECT 
    YEAR(date_order) AS 'Рік',
    MONTH(date_order) AS 'Місяць',
    COUNT(DISTINCT patient_order) AS 'Кількість замовлень',
    ROUND(SUM(cost_real), 2) AS 'Доход, грн.'
FROM base.raw_data 
WHERE date_order BETWEEN '2018-01-01' AND '2023-12-31'
GROUP BY 
    YEAR(date_order),
    MONTH(date_order)
ORDER BY 
    YEAR(date_order),
    MONTH(date_order); -- Кількість замовлень та доходи помісячно за всі роки
SELECT SUM(order_count) 
FROM (
	SELECT patient, birthday, COUNT(DISTINCT patient_order) AS order_count 
    FROM base.raw_data 
    WHERE date_order 
    BETWEEN '2018-01-01' AND '2023-06-30' 
    GROUP BY patient, birthday) AS S1; -- Кількість замовлень у червні (правильно)