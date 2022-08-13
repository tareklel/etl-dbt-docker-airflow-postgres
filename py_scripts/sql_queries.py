# from source database to staging
suppliers_query = "COPY (SELECT * FROM source.suppliers) TO '/staging/suppliers.csv' WITH CSV HEADER;"
products_query = "COPY (SELECT * FROM source.products) TO '/staging/products.csv' WITH CSV HEADER;"
customers_query = "COPY (SELECT * FROM source.customers) TO '/staging/customers.csv' WITH CSV HEADER;"
company_query = "COPY (SELECT * FROM source.company) TO '/staging/company.csv' WITH CSV HEADER;"
customer_order_query = "COPY (SELECT * FROM source.customer_order) TO '/staging/customer_order.csv' WITH CSV HEADER;"
company_order_query = "COPY (SELECT * FROM source.company_order) TO '/staging/company_order.csv' WITH CSV HEADER;"
supplier_inventory_query = "COPY (SELECT * FROM source.supplier_inventory) TO '/staging/supplier_inventory.csv' WITH CSV HEADER;"
company_catalogue_query = "COPY (SELECT * FROM source.company_catalogue) TO '/staging/company_catalogue.csv' WITH CSV HEADER;"

# from staging to source databas
dest_suppliers = "truncate table staging.suppliers; copy staging.suppliers FROM '/staging/suppliers.csv' WITH CSV HEADER;"
dest_products = "truncate table staging.products; copy staging.products FROM '/staging/products.csv' WITH CSV HEADER;" 
dest_customers = "truncate table staging.customers; copy staging.customers FROM '/staging/customers.csv' WITH CSV HEADER;" 
dest_company = "truncate table staging.company; copy staging.company FROM '/staging/company.csv' WITH CSV HEADER;"
dest_customer_order = "truncate table staging.customer_order; copy staging.customer_order FROM '/staging/customer_order.csv' WITH CSV HEADER;"
dest_company_order = "truncate table staging.company_order; copy staging.company_order FROM '/staging/company_order.csv' WITH CSV HEADER;"
dest_supplier_inventory = "truncate table staging.supplier_inventory; copy staging.supplier_inventory FROM '/staging/supplier_inventory.csv' WITH CSV HEADER;"
dest_company_catalogue = "truncate table staging.company_catalogue; copy staging.company_catalogue FROM '/staging/company_catalogue.csv' WITH CSV HEADER;"

# logs to database
dest_logs_init = "truncate table staging.access_logs;"
dest_logs = "copy staging.access_logs FROM '/staging/{0}' with CSV HEADER;"