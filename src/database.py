import sqlite3


def set_up():
    try:
        connection = sqlite3.connect('test.db')
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS sensor(id INTEGER PRIMARY KEY AUTOINCREMENT,'
                       'timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,'
                       'temperature REAL,'
                       'humidity REAL,'
                       'pressure REAL,'
                       'tvoc INTEGER,'
                       'eco2 INTEGER,'
                       'cpu_temp REAL);')
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print(error)
    finally:
        if connection:
            connection.close()
