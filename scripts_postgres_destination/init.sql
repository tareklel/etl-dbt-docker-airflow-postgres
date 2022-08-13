CREATE SCHEMA IF NOT EXISTS staging;
CREATE TABLE IF NOT EXISTS staging.suppliers (supplier_cuit int NOT NULL, supplier_name varchar);
CREATE TABLE IF NOT EXISTS staging.products (product_id int NOT NULL, product_name varchar);
CREATE TABLE IF NOT EXISTS staging.customers (doc_number int NOT NULL, fullname varchar, dob date);
CREATE TABLE IF NOT EXISTS staging.company (company_cuit int NOT NULL, company_name varchar);
CREATE TABLE IF NOT EXISTS staging.customer_order (customer_order_id int NOT NULL, doc_number int NOT NULL,
                                                            company_cuit int NOT NULL,
                                                            product_id int NOT NULL,
                                                            country varchar,
                                                            payment_amount numeric(10,2),
                                                            quantity_bought int,
                                                            order_date date);
CREATE TABLE IF NOT EXISTS staging.company_order (company_order_id int NOT NULL,
                                                            supplier_cuit int NOT NULL,
                                                            company_cuit int NOT NULL,
                                                            product_id int NOT NULL,
                                                            payment_amount numeric(10,2),
                                                            quantity_bought int,
                                                            order_date date);
CREATE TABLE IF NOT EXISTS staging.supplier_inventory (supplier_inventory_id int NOT NULL,
                                                            supplier_cuit int NOT NULL,
                                                            product_id int NOT NULL,
                                                            number_items int,
                                                            price_per_unit numeric(10,2));
CREATE TABLE IF NOT EXISTS staging.company_catalogue (company_catalogue_id int NOT NULL,
                                                            company_cuit int NOT NULL,
                                                            product_id int NOT NULL,
                                                            number_items int,
                                                            price_per_unit numeric(10,2));

CREATE TABLE IF NOT EXISTS staging.access_logs (ip_address varchar NOT NULL, username varchar, log_time time, useragent varchar);

CREATE SCHEMA IF NOT EXISTS dbt_dwh;
CREATE TABLE IF NOT EXISTS dbt_dwh.ip_to_country (ip_address_start bigint,ip_address_end bigint,country_code varchar,country varchar);
\copy dbt_dwh.ip_to_country FROM '/seed/IP2LOCATION-LITE-DB1.CSV' with CSV HEADER;
