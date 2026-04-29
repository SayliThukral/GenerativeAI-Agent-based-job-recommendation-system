import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

try:
    # Existing table mein naya column 'user_plan' add kar rahe hain
    cursor.execute("ALTER TABLE users ADD COLUMN user_plan TEXT DEFAULT 'None'")
    print("Success!.")
except sqlite3.OperationalError as e:
    print(" Error:", e)

conn.commit()
conn.close()