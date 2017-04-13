import sqlite3
conn = sqlite3.connect('DIBS.db')
c = conn.cursor()

class Database_Creation: 
    c.execute('''CREATE TABLE user_points
             (user, points)''')

    c.execute("INSERT INTO user_points VALUES ('Alex',200)")

    for row in c.execute('SELECT * FROM user_points ORDER BY points'):
        print(row)

    # Cleanup
    conn.commit()
    conn.close()