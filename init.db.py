import sqlite3

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task_text TEXT NOT NULL
)
''')
conn.commit()
conn.close()
print("Database initialized.")
