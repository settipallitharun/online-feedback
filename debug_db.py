import sqlite3
import os

# Check if database exists
if os.path.exists('database.db'):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        print('Users table exists')
        cursor.execute('SELECT id, name, email, is_admin FROM users')
        users = cursor.fetchall()
        print(f'Found {len(users)} users:')
        for user in users:
            print(f'  ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Admin: {user[3]}')
    else:
        print('Users table does not exist!')
    
    conn.close()
else:
    print('Database does not exist!')
