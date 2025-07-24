import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

def analyze_data():
    try:
        
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "ecommerce_nigeria"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )
        
        
        queries = {
            "total_revenue": "SELECT SUM(quantity * price) AS revenue FROM sales;",
            "top_products": """
                SELECT product, SUM(quantity) AS total_quantity
                FROM sales
                GROUP BY product
                ORDER BY total_quantity DESC
                LIMIT 5;
            """,
            "customer_analysis": """
                SELECT customer_id, SUM(quantity * price) AS total_spent
                FROM sales
                GROUP BY customer_id
                ORDER BY total_spent DESC
                LIMIT 5;
            """
        }
        
        
        results = {}
        for name, query in queries.items():
            results[name] = pd.read_sql(query, conn)
        
        
        print("\n تقرير تحليل المبيعات:")
        print(f" إجمالي الإيرادات: ${results['total_revenue'].iloc[0]['revenue']:,.2f}")
        
        print("\n أفضل 5 منتجات مبيعاً:")
        print(results['top_products'].to_markdown(index=False))
        
        print("\n أفضل 5 عملاء من حيث الإنفاق:")
        print(results['customer_analysis'].to_markdown(index=False))
        
        
        plot_top_products(results['top_products'])
        
    except Exception as e:
        print(f" خطأ في التحليل: {e}")
    finally:
        if conn:
            conn.close()

def plot_top_products(df):
    plt.figure(figsize=(10, 6))
    plt.bar(df['product'], df['total_quantity'])
    plt.title('أفضل المنتجات مبيعاً')
    plt.xlabel('المنتج')
    plt.ylabel('الكمية المباعة')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('top_products.png')
    print("\n تم حفظ الرسم البياني في top_products.png")

if _name_ == "_main_":
    analyze_data()
