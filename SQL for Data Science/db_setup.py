

import sqlite3
import pandas as pd

def setup_database(db_name="bookcycle.db"):
       
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Creating books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                genre TEXT,
                price REAL,
                stock INTEGER
            )
        ''')

        # Creating customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                join_date TEXT,
                is_member INTEGER,
                zip_code INTEGER,
                birth_year INTEGER,
                preferred_store TEXT
            )
        ''')

        # Creating transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                book_id INTEGER,
                purchase_date TEXT,
                quantity INTEGER,
                total_price REAL,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
        ''')

        conn.commit()

        # Loading data from CSVs
        books_df = pd.read_csv("books.csv")
        customers_df = pd.read_csv("customers.csv")
        transactions_df = pd.read_csv("transactions.csv")

        # Inserting data into tables
        books_df.to_sql("books", conn, if_exists="replace", index=False)
        customers_df.to_sql("customers", conn, if_exists="replace", index=False)
        transactions_df.to_sql("transactions", conn, if_exists="replace", index=False)

        conn.close()
        print("✅ Database setup complete: Tables created and populated with data!")

    # Example usage:
    # setup_database()  # Call this from the first notebook

