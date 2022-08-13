{{ config(
    tags=["sourcePostgres"]
) }}

select 
    customer_order_id, 
    c.doc_number, 
    c.fullname, 
    co.company_name, 
    country as customer_country, 
    p.product_name, payment_amount, 
    order_date,
    quantity_bought 
from 
    {{ref('customer_order')}} o 
left join {{ref('customers')}} c on c.doc_number = o.doc_number 
left join {{ref('company')}} co on co.company_cuit = o.company_cuit 
left join {{ref('products')}} p on p.product_id = o.product_id