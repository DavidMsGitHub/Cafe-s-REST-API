conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cafe ORDER BY RANDOM()')
    random_coffee = cursor.fetchone()