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


def add_sensor_data(temp, hum, pres, tvoc, eco2, cpu_temp):
    query(
        'INSERT INTO sensor(temperature, humidity, pressure, tvoc, eco2, cpu_temp) VALUES ('
        + str(temp) + ',' + str(hum) + ',' + str(pres) + ',' + str(tvoc) + ',' + str(eco2) + ',' + str(cpu_temp) + ')')


def get_avg_data():
    result = query(
        'SELECT AVG(temperature), AVG(humidity), AVG(pressure), AVG(tvoc), AVG(eco2), AVG(cpu_temp) FROM sensor;')
    average = {}
    for row in result:
        average = {
            "temperature": row[0],
            "humidity": row[1],
            "pressure": row[2],
            "tvoc": row[3],
            "eco2": row[4],
            "cpu_temp": row[5]
        }
    return average
