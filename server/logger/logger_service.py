import inspect
import json
import os
import sqlite3
from datetime import datetime
from flask_login import current_user
from server import configuration
from server.constants.error_constants import ErrorConstant
from server.logger.logger_constants.enum_level import LoggerLevel


def info(ex, username=None):
    _log(ex, LoggerLevel.info, username)


def warning(ex, username=None):
    _log(ex, LoggerLevel.warning, username)


def error(ex, username=None):
    _log(ex, LoggerLevel.error, username)


def critical(ex, username=None):
    _log(ex, LoggerLevel.critical, username)


def _log(ex, level: LoggerLevel, username=None):
    try:
        if type(ex) is dict:
            message = json.dumps(ex)
        elif type(ex) is ErrorConstant:
            message = ex.value
        else:
            message = str(ex)

        if level.value >= configuration.print_from_level:
            print(message)

        call_by = inspect.stack()
        if username is None:
            try:
                username = current_user.get_user_name()
            except:
                username = None
        values = [level.value, message, datetime.now(), username]
        for i in range(6):
            if len(call_by) > i + 2:
                values.append(call_by[i + 2].function)
                values.append(call_by[i + 2].filename)
            else:
                values.append(None)
                values.append(None)

        write(values)
    except Exception as error:
        print(message, level, error)


def write(values):
    check_if_database_exist()
    connection = sqlite3.connect(configuration.sql_name)
    cursor = connection.cursor()
    query = '''INSERT INTO logs 
                    (level, message, time, username,
                    caller_1, caller_1_location,  
                    caller_2, caller_2_location,  
                    caller_3, caller_3_location,  
                    caller_4, caller_4_location,  
                    caller_5, caller_5_location,  
                    caller_6, caller_6_location)  
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cursor.execute(query, values)
    connection.commit()
    cursor.close()


def check_if_database_exist():
    retval = os.path.exists(configuration.sql_name)
    if not retval:
        connection = sqlite3.connect(configuration.sql_name)
        cursor = connection.cursor()
        cursor.execute(table)
        cursor.close()
    return retval


table = """CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time datetime DEFAULT(DATE()) not null,
    level int not null,
    message nvarchar(1000) not null,
    username nvarchar(50) null,
    caller_1 nvarchar(30) not null,
    caller_1_location nvarchar(50) not null,
    caller_2 nvarchar(30) null,
    caller_2_location nvarchar(50) null,
    caller_3 nvarchar(30) null,
    caller_3_location nvarchar(50) null,
    caller_4 nvarchar(30) null,
    caller_4_location nvarchar(50) null,
    caller_5 nvarchar(30) null,
    caller_5_location nvarchar(50) null,
    caller_6 nvarchar(30) null,
    caller_6_location nvarchar(50) null
);"""
