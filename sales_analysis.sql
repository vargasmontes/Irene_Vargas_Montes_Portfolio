-- ==== ReadMe ====
-- This is an eCommerce Sales Dataset from Kaggle available here: https://www.kaggle.com/datasets/abbas829/ecommerce-sales-dataset?resource=download
-- We will be looking at some questions that the data helps answer.
-- This is code for SQL Server

-- ==== Rename imported database and get information on it ====
EXEC sp_rename 'portfolio_sales_data', 'sales'
SELECT * from sales
exec sp_help sales

-- ==== Filtering for different information ====
SELECT * FROM sales WHERE customer_id = 1130 -- One customer's purchases
SELECT * FROM sales WHERE region = 'West' AND delivery_days > 3 AND customer_rating < 20 -- Customers from West whose orders took more than three days and got bad reviews

-- ==== Analysing the data ====
SELECT AVG(revenue) AS avg_order_value FROM sales -- Average order value
SELECT AVG(unit_price) AS avg_unit_price FROM sales -- Average unit price
SELECT region, product_category, COUNT(order_id) AS order_amount, SUM(revenue) AS subtotal FROM sales GROUP BY region, product_category ORDER BY region -- Revenue and number of orders per region
SELECT TOP 5 order_date, SUM(revenue) AS day_revenue FROM sales GROUP BY order_date ORDER BY day_revenue DESC -- Most profitable day
SELECT TOP 10 RANK() OVER (ORDER BY SUM(revenue) DESC) AS spend_rank, customer_id, SUM(revenue) AS total_spent FROM sales GROUP BY customer_id -- Best customers
SELECT payment_method, COUNT(payment_method) AS order_amount FROM sales GROUP BY payment_method ORDER BY order_amount DESC-- Most popular form of payment
SELECT order_date, SUM(revenue) OVER (ORDER BY order_date) AS running_revenue FROM sales -- Running revenue over time

-- Revenue per region and percentage of the total
WITH regional_totals AS (
    SELECT region, SUM(revenue) AS total_revenue
    FROM sales
    GROUP BY region
)
SELECT region, total_revenue,
       total_revenue * 100.0 / SUM(total_revenue) OVER () AS percentage_of_total
FROM regional_totals

-- Find customers who've ordered more than once
SELECT customer_id, COUNT(order_id) AS order_count
FROM sales
GROUP BY customer_id
HAVING COUNT(order_id) > 1