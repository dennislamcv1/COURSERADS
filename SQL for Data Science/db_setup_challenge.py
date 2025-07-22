

import sqlite3
import pandas as pd

def setup_database(db_name="product_catalog.db"):
       
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Creating products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                city TEXT,
                product_url TEXT,
                tags TEXT,
                product_picture TEXT
            )
        ''')

        conn.commit()

        # Loading data from CSVs
        products_df = pd.read_csv("products.csv")
        
        # Inserting data into tables
        products_df.to_sql("products", conn, if_exists="replace", index=False)
        
        conn.close()
        #print("✅ Database setup complete)

    # Example usage:
    # setup_database()  # Call this from the first notebook

