import sqlite3

# Update existing user email to lowercase
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Update existing emails to lowercase
cursor.execute('UPDATE users SET email = LOWER(email)')

conn.commit()

# Check the updated data
cursor.execute('SELECT id, name, email, is_admin FROM users')
users = cursor.fetchall()
print('Updated users:')
for user in users:
    print(f'  ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Admin: {user[3]}')

conn.close()
print('Email case fixed!')
