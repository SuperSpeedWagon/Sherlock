#!venv/bin/python3
# -*- coding: utf-8 -*-
__author__ = "Benjamin Trubert, Kévin Huguenin, Alpha Diallo, Lev Velykoivanenko, Noé Zufferey"
__copyright__ = "Copyright 2021, The Information Security and Privacy Lab at the University of Lausanne (" \
                "https://www.unil.ch/isplab/)"
__credits__ = ["Benjamin Trubert", "Kévin Huguenin", "Alpha Diallo", "Lev Velykoivanenko", "Noé Zufferey",
               "Vaibhav Kulkarni"]

__version__ = "1"
__license__ = "MIT"
__maintainer__ = "Kévin Huguenin"
__email__ = "kevin.huguenin@unil.ch"

import sqlite3
import datetime
from datetime import timezone
from location import *


class WifiLogsLocationProvider(ListLocationProvider):

    def __init__(self, dbName: str, wifiUsername: str):
        self.__dbName = dbName
        self.__wifiUsername = wifiUsername
        self.__list_location_sample = self.__build_list_location_sample()

    def __build_list_location_sample(self):
        con = sqlite3.connect(self.__dbName)
        cur = con.cursor()

        sql_query = "SELECT timestamp, latitude, longitude " \
                    "FROM users AS u " \
                    "INNER JOIN location_samples AS ls " \
                    "ON u.id = ls.uid " \
                    "INNER JOIN hotspots AS h " \
                    "ON h.id = ls.hid " \
                    "WHERE u.name = '{name:s}' " \
                    "ORDER BY timestamp".format(name=self.__wifiUsername)
        query_results = cur.execute(sql_query)
        print("----------------->", query_results.fetchone())
        ls = []
        for timestamp, lat, lng in query_results:
            print(timestamp, lat, lng)
            loc = Location(lat, lng)
            dt = datetime.fromtimestamp(timestamp)
            ls += [LocationSample(dt, loc)]

        con.close()
        return ls

    def __str__(self):
        res = ""
        for ls in self.__list_location_sample:
            res += str(ls) + "\n"
        return res

    # TODO: (Optionnel) Redéfinir la méthode
    #       get_surrounding_temporal_location_sample pour effectuer les calculs
    #       dans la requête SQL.
    def get_surrounding_temporal_location_sample(self, timestamp: int):
        con = sqlite3.connect(self.__dbName)
        cur = con.cursor()
        ops = [(">", "ASC"), ("<=", "DESC")]
        prev = next_ = None
        for op, order in ops:
            sql_query = "SELECT timestamp, latitude, longitude " \
                        "FROM users AS u " \
                        "INNER JOIN location_samples AS ls " \
                        "ON u.id = ls.uid " \
                        "INNER JOIN hotspots AS h " \
                        "ON h.id = ls.hid " \
                        "WHERE u.name = '{name:s}' AND ls.timestamp {op:s} {timestamp:d} " \
                        "ORDER BY timestamp {order:s} " \
                        "LIMIT 1".format(
                name=self.__wifiUsername,
                timestamp=timestamp,
                op=op,
                order=order
            )
            query_result = cur.execute(sql_query).fetchone()
            if len(query_result):
                timestamp, lat, lng = query_result
                loc = Location(lat, lng)
                dt = datetime.fromtimestamp(timestamp)
                if op == ">":
                    next_ = LocationSample(dt, loc)
                elif op == "<=":
                    prev = LocationSample(dt, loc)

        return prev, next_


if __name__ == '__main__':
    # Tester l'implémentation de cette classe avec les instructions de ce bloc
    # main (le résultat attendu est affiché ci-dessous).

    Configuration.get_instance().add_element("verbose", True)
    lp = WifiLogsLocationProvider('../data/db/wifi.db', 'ljohnson')
    print(lp)
    lp.show_location_samples()

    ### Résultat attendu ###

    # WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'ljohnson', 2 location samples)
    # #WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'ljohnson', 2 location samples)
