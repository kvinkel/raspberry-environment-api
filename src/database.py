import sqlite3
import os


def query(sql):
    try:
        if os.path.isdir('sqlite_db'):
            connection = sqlite3.connect('/sqlite_db/sqlite.db')
        else:
            connection = sqlite3.connect('sqlite.db')
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
    query('CREATE TABLE IF NOT EXISTS sgp30_baseline(timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,'
          ' eco2 INTEGER, tvoc Integer);')
    count = query('SELECT COUNT(*) FROM sgp30_baseline')
    if count[0][0] == 0:
        query('INSERT INTO sgp30_baseline(eco2, tvoc) VALUES (0, 0);')


def add_sensor_data(temp, hum, pres, tvoc, eco2, cpu_temp):
    query('INSERT INTO sensor(temperature, humidity, pressure, tvoc, eco2, cpu_temp) VALUES (' + str(temp) + ','
          + str(hum) + ',' + str(pres) + ',' + str(tvoc) + ',' + str(eco2) + ',' + str(cpu_temp) + ');')


def get_avg_data():
    result = query('SELECT AVG(temperature), AVG(humidity), AVG(pressure), AVG(tvoc), AVG(eco2), AVG(cpu_temp) FROM sensor;')
    average = {
        "temperature": result[0][0],
        "humidity": result[0][1],
        "pressure": result[0][2],
        "tvoc": result[0][3],
        "eco2": result[0][4],
        "cpu_temp": result[0][5]
    }
    return average


def get_min_max():
    result = query('SELECT MIN(temperature), MIN(humidity), MIN(pressure), MIN(tvoc), MIN(eco2), MIN(cpu_temp),'
                   ' MAX(temperature), MAX(humidity), MAX(pressure), MAX(tvoc), MAX(eco2), MAX(cpu_temp) FROM sensor;')
    min_max = {
        "min_temp": result[0][0],
        "min_hum": result[0][1],
        "min_press": result[0][2],
        "min_tvoc": result[0][3],
        "min_eco2": result[0][4],
        "min_cpu_temp": result[0][5],
        "max_temp": result[0][6],
        "max_hum": result[0][7],
        "max_press": result[0][8],
        "max_tvoc": result[0][9],
        "max_eco2": result[0][10],
        "max_cpu_temp": result[0][11]
    }
    return min_max


def get_measurement_info():
    result = query('SELECT MIN(timestamp), MAX(timestamp), COUNT(*) FROM sensor;')
    info = {
        "first_measurement": result[0][0],
        "latest_measurement": result[0][1],
        "total_measurements": result[0][2]
    }
    return info


def set_baseline(eco2, tvoc):
    query('UPDATE sgp30_baseline SET timestamp = CURRENT_TIMESTAMP, eco2 = ' + str(eco2) + ', tvoc = ' + str(tvoc) + ';')


def get_baseline():
    return query('SELECT eco2, tvoc FROM sgp30_baseline;')[0]
