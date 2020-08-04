import sqlite3


def query(sql):
    try:
        connection = sqlite3.connect('test.db')
        cursor = connection.cursor()
        result = cursor.execute(sql).fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return result
    except sqlite3.Error as error:
        print(error)
    finally:
        if connection:
            connection.close()


def set_up():
    query('CREATE TABLE IF NOT EXISTS sensor(id INTEGER PRIMARY KEY AUTOINCREMENT,'
          'timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,'
          'temperature REAL,'
          'humidity REAL,'
          'pressure REAL,'
          'tvoc INTEGER,'
          'eco2 INTEGER,'
          'cpu_temp REAL);')
