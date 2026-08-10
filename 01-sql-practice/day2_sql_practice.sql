customers(
    customer_id,
    name,
    city,
    signup_date
);

orders(
    order_id,
    customer_id,
    order_date,
    amount,
    status
);

products(
    product_id,
    product_name,
    category,
    price
);

order_items(
    order_item_id,
    order_id,
    product_id,
    quantity
);