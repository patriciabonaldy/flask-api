""" Autor: Patricia Bonaldy
    Email: pbonaldy@afip.gob.ar
    
"""
import cx_Oracle
from oracle_util import config

""" ------------------------------------------------------------------ """
""" Oracle """


def get_connection(user, pwd):
    """ Obtiene la conexion a Oracle """
    try:
        connection = cx_Oracle.connect(user + '/' + pwd + '@' + 
                                       config.FISCO_CONNECTION_STRING)
        connection.autocommit = False
        print('Connection Opened')
        return connection
    except Exception as e:
        print('Exception: ' + str(e))


def close_connection(connection):
    """ Cierra la conexion a Oracle """
    try:
        if connection is not None:
            connection.close()
            print('Connection Closed')
    except Exception as e:
        print('Exception: ' + str(e))


def execute_consulta(consulta):
    """ DB Cnx """
    connection = get_connection(config.FISCO_USER, 
                                config.FISCO_FISCAR_PWD)
    reg = []

    if connection is not None:
        cursor_pe = connection.cursor()
        cursor_pe.execute(consulta)
        reg = cursor_pe.fetchone()
        cursor_pe.close()

    close_connection(connection)
    return reg