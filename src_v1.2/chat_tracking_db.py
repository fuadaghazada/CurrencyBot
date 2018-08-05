#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  11 16:14:04 2018

@author: fuadaghazada
"""

import sqlite3

# Connecting to SQLite3
def connect():
    try:
        connection = sqlite3.connect("chat_tracking.sqlite")

        return connection

    except Exception as e:
        print(e)
        return None

# Creates table with the given table_name
# @param table_name: given name or 'chat_info' as default

def create_table():
    try:
        connection = connect()

        sql_stmt = """
                    CREATE TABLE IF NOT EXISTS chat_info
                    (chat_id TEXT PRIMARY KEY, currency TEXT, schedule_state TEXT, schedule_currency TEXT, schedule_wait_time TEXT)
                   """
        #sql_chat_index = "CREATE INDEX IF NOT EXISTS chat_id_index ON chat_info (chat_id ASC)"

        connection.execute(sql_stmt)
        #connection.execute(sql_chat_index)
        connection.commit()
    except Exception as e:
        print(e)

# Adds new chat_id with additonal attributes which are null initially
# @param: given chat_id

def add_chat(chat_id):
    try:
        connection = connect()

        sql_stmt = """
                    INSERT INTO chat_info (chat_id, currency, schedule_state, schedule_currency, schedule_wait_time)
                    VALUES ((?), null, null, null, null)
                   """
        args = (chat_id,)
        connection.execute(sql_stmt, args)
        connection.commit()

        return True
    except Exception as e:
        return None

# Updates the given attribute of table (chat_info) with the given value for the attribute.
# @param chat_id: the given chat_id
# @param attr: the given attribute of the table
# @param value: the given value for the given attribute

def update_chat(chat_id, attr, value):
    try:
        connection = connect()

        sql_stmt = "UPDATE chat_info SET {} = (?) WHERE chat_id = (?)".format(attr)
        args = (value, chat_id,)
        connection.execute(sql_stmt, args)
        connection.commit()

        return True
    except Exception as e:
        return None



# Gets the element got from the table with the given attribute
# @param attr: the given attribute for the table
# @return: result of the query in list

def get_elements(attr, chat_id = None):
    try:
        connection = connect()

        if chat_id:
            stmt = "SELECT {} FROM chat_info WHERE chat_id = (?)".format(attr)
            args = (chat_id,)

            result = [x[0] for x in connection.execute(stmt, args)]

            if len(result) == 0:
                return None
            else:
                return [x[0] for x in connection.execute(stmt, args)]
        else:
            stmt = "SELECT {} FROM chat_info".format(attr)

            return [x[0] for x in connection.execute(stmt)]
    except Exception as e:
        return None


def print_everything():
    connection = connect()

    for x in connection.execute("SELECT * FROM chat_info"):
        print(x)

# print_everything()

# print("asdfghjkl")
