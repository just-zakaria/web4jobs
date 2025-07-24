import pandas as pd
import psycopg2

df = pd.read_csv("ecommerce_data.csv")

conn = psycopg2.connect(
    dbname="ecommerce_nigeria",
    user="postgres",
    password="mot_de_passe_ici",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
    DROP TABLE IF EXISTS sales;
    CREATE TABLE sales (
        order_id INT PRIMARY KEY,
        customer_id TEXT,
        order_date DATE,
        product TEXT,
        quantity INT,
        price NUMERIC
    );
""")

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO sales (order_id, customer_id, order_date, product, quantity, price)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))

conn.commit()
cur.close()
conn.close()
print("✅ البيانات ترفعات بنجاح.")
