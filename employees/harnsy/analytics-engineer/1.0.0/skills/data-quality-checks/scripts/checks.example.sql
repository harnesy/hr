-- Example checks. Each returns the rows that break the rule; zero rows = pass.
-- Tables assumed: customers(id, country, created_at), orders(id, customer_id, status, amount).

-- check: orders.id is unique
SELECT id, COUNT(*) AS copies
FROM orders
GROUP BY id
HAVING COUNT(*) > 1;

-- check: orders.customer_id is not null
SELECT id
FROM orders
WHERE customer_id IS NULL;

-- check: orders.status has only allowed values
SELECT id, status
FROM orders
WHERE status NOT IN ('new', 'paid', 'shipped', 'cancelled');

-- check: every order points to an existing customer
SELECT o.id, o.customer_id
FROM orders o
LEFT JOIN customers c ON c.id = o.customer_id
WHERE o.customer_id IS NOT NULL AND c.id IS NULL;

-- check: order amounts are not negative
SELECT id, amount
FROM orders
WHERE amount < 0;
