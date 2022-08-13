CREATE SCHEMA IF NOT EXISTS source;
CREATE TABLE IF NOT EXISTS source.suppliers (supplier_cuit int PRIMARY KEY, supplier_name varchar);
CREATE TABLE IF NOT EXISTS source.products (product_id SERIAL PRIMARY KEY, product_name varchar);
CREATE TABLE IF NOT EXISTS source.customers (doc_number int PRIMARY KEY, fullname varchar, dob date);
CREATE TABLE IF NOT EXISTS source.company (company_cuit int PRIMARY KEY, company_name varchar);
CREATE TABLE IF NOT EXISTS source.customer_order (customer_order_id serial PRIMARY KEY, doc_number int NOT NULL REFERENCES source.customers(doc_number),
                                                            company_cuit int NOT NULL REFERENCES source.company(company_cuit),
                                                            product_id int NOT NULL REFERENCES source.products(product_id),
                                                            country varchar,
                                                            payment_amount numeric(10,2),
                                                            quantity_bought int,
                                                            order_date date);
CREATE TABLE IF NOT EXISTS source.company_order (company_order_id serial PRIMARY KEY,
                                                            supplier_cuit int NOT NULL REFERENCES source.suppliers(supplier_cuit),
                                                            company_cuit int NOT NULL REFERENCES source.company(company_cuit),
                                                            product_id int NOT NULL REFERENCES source.products(product_id),
                                                            payment_amount numeric(10,2),
                                                            quantity_bought int,
                                                            order_date date);
CREATE TABLE IF NOT EXISTS source.supplier_inventory (supplier_inventory_id serial PRIMARY KEY,
                                                            supplier_cuit int NOT NULL REFERENCES source.suppliers(supplier_cuit),
                                                            product_id int NOT NULL REFERENCES source.products(product_id),
                                                            number_items int,
                                                            price_per_unit numeric(10,2));
CREATE TABLE IF NOT EXISTS source.company_catalogue (company_catalogue_id serial PRIMARY KEY,
                                                            company_cuit int NOT NULL REFERENCES source.company(company_cuit),
                                                            product_id int NOT NULL REFERENCES source.products(product_id),
                                                            number_items int,
                                                            price_per_unit numeric(10,2));
INSERT INTO source.suppliers (supplier_cuit, supplier_name) VALUES (100, 'supplier1'), (200, 'supplier2');
INSERT INTO source.products (product_name) VALUES ('product1'), ('product2');
INSERT INTO source.customers (doc_number, fullname, dob) VALUES (111, 'John Smith', '1990-09-01'), (222, 'Jane Lane', '1980-02-13'),(333, 'Dubois Phillips', '1985-03-23');
INSERT INTO source.company (company_cuit, company_name) VALUES (777, 'company1'), (888, 'company2');
INSERT INTO source.customer_order (doc_number, company_cuit, product_id, country, 
                    payment_amount, quantity_bought, order_date)
                    VALUES (111, 777, 1, 'United States of America', 200, 1, '2022-01-01'),
                    (222, 888, 2, 'Italy', 300, 1, '2022-02-01'),
                    (333, 777, 2, 'China', 600, 2, '2022-02-22'),
                    (333, 777, 2, 'Germany', 600, 2, '2022-03-22');

INSERT INTO source.company_order (supplier_cuit, company_cuit, product_id, 
                    payment_amount, quantity_bought, order_date)
                    VALUES (100, 777, 1, 100, 1, '2021-01-01'),
                    (100, 888, 2, 150, 1, '2021-02-01'),
                    (200, 777, 2, 155, 2, '2021-02-22');

INSERT INTO source.supplier_inventory (supplier_cuit, product_id, number_items, price_per_unit)
                                VALUES (100, 1, 5, 100), (100, 2, 10, 50), (200, 2, 20, 50)
                                ;
INSERT INTO source.company_catalogue (company_cuit, product_id, number_items, price_per_unit)
                               VALUES (777, 1, 4, 200), (777, 2, 3, 100), (888, 2, 4, 100);