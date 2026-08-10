# Day 2 - SQL and Python Pipeline Strengthening

## Today’s Goal
Improve SQL and Python pipeline skills for AI Data Engineering.

## Topics
- SQL joins
- CTEs
- Window functions
- Duplicate detection
- Python ETL structure
- Logging
- Error handling


## Day 2 Python Pipeline Questions

### 1. What does `load_csv()` do?

`load_csv()` reads a CSV file and loads it into a pandas DataFrame. It is used to load input files such as `customers.csv` and `orders.csv`.

---

### 2. Why do we use `try/except`?

We use `try/except` to handle errors safely. If a file is missing or cannot be loaded, the program logs an error message instead of failing silently. This makes the pipeline easier to debug.

---

### 3. What does `clean_orders()` do?

`clean_orders()` cleans the orders data. It removes duplicate rows, removes rows where `amount` is missing, keeps only completed orders, and converts `order_date` into a proper datetime format.

---

### 4. Why do we remove duplicates?

We remove duplicates to avoid counting the same order more than once. Duplicate records can create incorrect totals, wrong customer spending, and inaccurate monthly revenue.

---

### 5. Why do we remove rows where amount is missing?

We remove rows where `amount` is missing because revenue calculations require a valid amount. If the amount is missing, we cannot correctly calculate customer spending or monthly revenue.

---

### 6. Why do we keep only completed orders?

We keep only completed orders because revenue should usually be calculated from successful transactions. Pending or cancelled orders should not be included in final revenue calculations.

---

### 7. What does `validate_customer_ids()` check?

`validate_customer_ids()` checks whether every `customer_id` in the orders data exists in the customers data. It helps identify orders that belong to invalid or missing customers.

---

### 8. Why is customer_id 107 invalid?

Customer ID `107` is invalid because it appears in `orders.csv`, but it does not exist in `customers.csv`. This means the order has no matching customer record.

---

### 9. What does `create_customer_summary()` produce?

`create_customer_summary()` creates a summary of total spending for each customer. It combines customer information with the total amount spent from completed orders.

---

### 10. Why do we use `how="left"` in `merge()`?

We use `how="left"` so that all customers remain in the final customer summary, even if they did not place any completed orders. Customers with no completed spending will still appear with a value of `0`.

---

### 11. What does `create_monthly_summary()` produce?

`create_monthly_summary()` creates monthly revenue totals. It groups completed orders by month and calculates the total revenue for each month.

---

### 12. What does `save_output()` do?

`save_output()` saves a DataFrame as a CSV file inside the `output` folder. It also creates the output folder if it does not already exist.

---

### 13. Why is logging better than only using `print()`?

Logging is better than `print()` because it gives structured messages with timestamps and log levels such as `INFO`, `WARNING`, and `ERROR`. This is useful in real data pipelines because it helps track what the pipeline is doing and where issues happen.

---

### 14. How is this related to AI Data Engineering?

This pipeline is related to AI Data Engineering because AI systems also need clean, validated, and structured data before they can use it. Today we processed CSV data, but later the same idea will apply to AI pipelines: documents will be extracted, cleaned, validated, chunked, embedded, and stored in a vector database for RAG applications.

## Reflection
What I completed:

What was easy:

What was difficult:

What I need to revise:

Tomorrow I should focus on: