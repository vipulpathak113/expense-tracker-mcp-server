from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'expenses.db')

mcp= FastMCP('Expnse Tracker')

def initialize_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)
initialize_db()

@mcp.tool()
def add_expense(amount, category, date, subcategory='', note=''):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO expenses (amount, category, date, subcategory, note)
            VALUES (?, ?, ?, ?, ?)
        """, (amount, category, date, subcategory, note))
        return {"status":"ok", "id": conn.lastrowid}     

@mcp.tool()    
def list_expenses():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT id,date,amount,category,subcategory,note FROM expenses ORDER BY id ASC")
        cols = [column[0] for column in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]     

if __name__ == "__main__":
    mcp.run()
