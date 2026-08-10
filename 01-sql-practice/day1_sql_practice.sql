-- Day 1 SQL Diagnostic Practice

-- Tables:
-- customers(customer_id, name, city, signup_date)
-- orders(order_id, customer_id, order_date, amount, status)

-- Q1. Find total revenue by customer.

select c.name,c.customer_id,  SUM(o.amount) AS total_revenue  from customers c join orders o ON  c.customer_id = o.customer_id GROUP BY c.customer_id, c.name;
-- Confidence: Easy / Medium / Hard / Need Revision


-- Q2. Find customers who placed more than 3 completed orders.
select c.customer_id, c.name, COUNT(o.order_id) AS completed_order_count from customers c
  JOIN orders o ON c.customer_id=o.customer_id 
  where LOWER(o.status)='completed'
  having COUNT(o.order_id)>3;

-- Confidence: Easy / Medium / Hard / Need Revision


-- Q3. Find the latest order for each customer.
SELECT 
    customer_id,
    name,
    order_id,
    order_date
FROM (
    SELECT 
        c.customer_id,
        c.name,
        o.order_id,
        o.order_date,
        ROW_NUMBER() OVER (
            PARTITION BY c.customer_id 
            ORDER BY o.order_date DESC
        ) AS rn
    FROM customers c
    JOIN orders o 
        ON c.customer_id = o.customer_id
) ranked_orders
WHERE rn = 1;

-- Confidence: Easy / Medium / Hard / Need Revision


-- Q4. Rank customers by total spending.

SELECT 
    c.customer_id,
    c.name,
    SUM(o.amount) AS total_spending,
    RANK() OVER (
        ORDER BY SUM(o.amount) DESC
    ) AS spending_rank
FROM customers c
JOIN orders o 
    ON c.customer_id = o.customer_id
GROUP BY 
    c.customer_id,
    c.name;
-- Confidence: Easy / Medium / Hard / Need Revision


-- Q5. Find monthly revenue.

SELECT 
    DATE_TRUNC('month', order_date) AS revenue_month,
    SUM(amount) AS monthly_revenue
FROM orders
WHERE LOWER(status) = 'completed'
GROUP BY 
    DATE_TRUNC('month', order_date)
ORDER BY 
    revenue_month;
-- Confidence: Easy / Medium / Hard / Need Revision


-- Q6. Find customers who signed up but never placed an order.
SELECT 
    c.customer_id,
    c.name,
    c.signup_date
FROM customers c
LEFT JOIN orders o 
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
-- Confidence: Easy / Medium / Hard / Need Revision


-- Q7. Find duplicate orders if the same customer placed the same amount on the same date.
SELECT 
    customer_id,
    order_date,
    amount,
    COUNT(*) AS duplicate_count
FROM orders
GROUP BY 
    customer_id,
    order_date,
    amount
HAVING COUNT(*) > 1;

-- Confidence: Easy / Medium / Hard / Need Revision