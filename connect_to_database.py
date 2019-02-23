import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

kDATABASE_NAME = 'vacationready'
kUSER = 'tushar'
kPASSWORD = 'password'

def get_database_connection():
    connection = psycopg2.connect(dbname = kDATABASE_NAME, user = kUSER, password = kPASSWORD, host = 'localhost')
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    return connection