#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 19:30:40 2018

@author: fuadaghazada
"""

import sqlite3

class DbHelper:

    def __init__(self, dbname="banksDB.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS atms (latitude longitude)"

        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, latitude, longitude):
        stmt = "INSERT INTO atms (latitude, longitude) VALUES (?, ?, ?)"
        args = (latitude, longitude, distance)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, attr):
        stmt = "DELETE FROM items WHERE attr = (?) AND owner = (?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT * FROM atms"
        return [x[0] for x in self.conn.execute(stmt)]
