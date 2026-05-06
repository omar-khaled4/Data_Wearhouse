-- Raw table for sales orders (from CSV files)
CREATE TABLE raw.orders (
    order_id        VARCHAR(50),
    customer_id     VARCHAR(50),
    product_id      VARCHAR(50),
    quantity        INTEGER,
    price           NUMERIC(10,2),
    order_date      VARCHAR(50),
    status          VARCHAR(50),
    loaded_at       TIMESTAMP DEFAULT NOW()
);

-- Raw table for customers (from database CDC)
CREATE TABLE raw.customers (
    customer_id     VARCHAR(50),
    customer_name   VARCHAR(100),
    email           VARCHAR(100),
    country         VARCHAR(50),
    signup_date     VARCHAR(50),
    loaded_at       TIMESTAMP DEFAULT NOW()
);

-- Raw table for application logs (from streaming)
CREATE TABLE raw.app_logs (
    log_id          VARCHAR(50),
    user_id         VARCHAR(50),
    event_type      VARCHAR(50),
    event_time      VARCHAR(50),
    page            VARCHAR(100),
    loaded_at       TIMESTAMP DEFAULT NOW()
);