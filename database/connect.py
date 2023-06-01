import psycopg2
import configparser


def get_connection():
    config = configparser.ConfigParser()
    config.read('database/config.ini')
    connect = None
    try:
        connect = psycopg2.connect(
            host=config['postgresql']['host'],
            database=config['postgresql']['database'],
            user=config['postgresql']['user'],
            password=config['postgresql']['password'])

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return connect