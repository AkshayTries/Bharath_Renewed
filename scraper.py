import os
import sqlite3

def create_db():
    conn = sqlite3.connect('data/scraped_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS web_pages (
            url TEXT PRIMARY KEY,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(filename, content):
    conn = sqlite3.connect('data/scraped_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO web_pages (url, content)
        VALUES (?, ?)
    ''', (filename, content))
    conn.commit()
    conn.close()

def process_txt_files(directory):
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    insert_data(filename, content)
        print("Text files processed and saved successfully.")
    except Exception as e:
        print(f"Error processing text files: {e}")

if __name__ == "__main__":
    create_db()
    process_txt_files("fodder/")
