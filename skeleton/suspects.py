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

import functools
import xml

import lxml.etree

from location import *
from pictures import *
from wifi import *
from twitter import *
from logs import *
from twitter import TwitterLocationProvider
import xml.etree.ElementTree as xml_et
import os
import json
from configuration import *


class Suspect:

    def __init__(self, name, locationProvider):
        self._name = name
        self._lp = locationProvider

    def get_name(self):
        return self._name

    def get_location_provider(self):
        return self._lp

    def __str__(self):
        return "[Suspect] Name: " + str(self._name) + ", Location provider: " + str(self._lp)

    # [Suspect] Name: jdoe, Location provider: PictureLocationProvider (source: ’ ../ data/pics /jdoe’ (JPG,JPEG,
    # jpg,jpeg), 2 location samples)

    @staticmethod
    def create_suspects_from_XML_file(filename: str):
        tree = xml.etree.ElementTree.parse(filename)
        root = tree.getroot()
        suspects = []
        for suspect in root.findall("suspect"):
            name = suspect.find("name").text
            loc: ListLocationProvider = []
            for src in suspect.find("sources"):
                if src.find("type").text == "Twitter":
                    loc.append(TwitterLocationProvider(src.find("username").text, src.find("token").text,
                                                       src.find("token_secret").text))
                elif src.find("type").text == "Photographs":
                    directory = src.find("dir").text
                    loc.append(PictureLocationProvider(directory))
                elif src.find("type").text == "Wi-Fi":
                    directory = src.find("db").text
                    loc.append(WifiLogsLocationProvider(directory, src.find("username").text))
                elif src.find("type").text == "Logs":
                    d = os.path.dirname(src.find("file").text)
                    directory = os.path.join(d, src.find("file").text)
                    loc.append(LogsLocationProvider(directory))
            l1 = loc.pop(0)
            l2 = loc.pop(0)
            composite = functools.reduce(lambda lp1, lp2: lp1 + lp2, loc,
                                         CompositeLocationProvider(l1, l2))
            suspects.append(Suspect(name, composite))
        return suspects

    # TODO: (Alternative) implémenter une méthode similaire pour les fichiers JSON
    @staticmethod
    def create_suspects_from_JSON_file(filename: str):
        pass


if __name__ == "__main__":
    # Tester l'implémentation de cette classe avec les instructions de ce bloc
    # main (le résultat attendu est affiché ci-dessous).

    Configuration.get_instance().add_element("verbose", False)
    Configuration.get_instance().add_element("crime_date", datetime.strptime("08/04/2021", "%d/%m/%Y").replace(tzinfo=timezone(timedelta(hours=2))))
    TwitterLocationProvider.set_api_key('Z4bLkruoqSp0JXJfJGTaMQEZo')
    TwitterLocationProvider.set_api_key_secret('gYyLCa7QiDje76VaTttlylDjGThCBGcp9MIcEGlzVq6FJcXIdc')
    #
    hardman = Suspect('chardman', PictureLocationProvider('../data/pics/chardman'))
    print(hardman)
    #
    suspects = Suspect.create_suspects_from_XML_file('../data/suspects.xml')
    print('\n'.join(map(str, suspects)))
    #
# suspects = Suspect.create_suspects_from_JSON_file('../data/suspects.json')
# print('\n'.join(map(str, suspects)))

### Résultat attendu ###

# [Suspect] Name: chardman, Location provider: PictureLocationProvider (source: '../data/pics/chardman' (JPG,JPEG,jpg,jpeg), 2 location samples)
# [Suspect] Name: Cyrus Hardman, Location provider: CompositeLocationProvider (5 location samples)
#  +	CompositeLocationProvider (2 location samples)
# 	 +	TwitterLocationProvider (user 'rvkint95' aka 'Verbal', 0 location samples)
# 	 +	PictureLocationProvider (source: '../data/pics/chardman' (JPG,JPEG,jpg,jpeg), 2 location samples)
#  +	WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'chardman', 3 location samples)
# [Suspect] Name: Linda Arden, Location provider: CompositeLocationProvider (9 location samples)
#  +	WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'larden', 3 location samples)
#  +	LogsLocationProvider (source: ../data/logs/larden.log, 6 location samples)
# [Suspect] Name: Hildegarde Schmidt, Location provider: CompositeLocationProvider (15 location samples)
#  +	CompositeLocationProvider (13 location samples)
# 	 +	PictureLocationProvider (source: '../data/pics/hschmidt' (JPG,JPEG,jpg,jpeg), 10 location samples)
# 	 +	LogsLocationProvider (source: ../data/logs/hschmidt.log, 3 location samples)
#  +	WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'hschmidt', 2 location samples)
# [Suspect] Name: Natalia Dragomiroff, Location provider: CompositeLocationProvider (16 location samples)
#  +	CompositeLocationProvider (13 location samples)
# 	 +	PictureLocationProvider (source: '../data/pics/ndragomiroff' (JPG,JPEG,jpg,jpeg), 9 location samples)
# 	 +	LogsLocationProvider (source: ../data/logs/ndragomiroff.log, 4 location samples)
#  +	WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'ndragomiroff', 3 location samples)
# [Suspect] Name: Hector MacQueen, Location provider: CompositeLocationProvider (16 location samples)
#  +	PictureLocationProvider (source: '../data/pics/hmacqueen' (JPG,JPEG,jpg,jpeg), 11 location samples)
#  +	WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'hmacqueen', 5 location samples)
# [Suspect] Name: Cyrus Hardman, Location provider: CompositeLocationProvider (5 location samples)
#  +	CompositeLocationProvider (2 location samples)
# 	 +	TwitterLocationProvider (user 'rvkint95' aka 'Verbal', 0 location samples)
# 	 +	PictureLocationProvider (source: '../data/pics/chardman' (JPG,JPEG,jpg,jpeg), 2 location samples)
#  +	WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'chardman', 3 location samples)
# [Suspect] Name: Linda Arden, Location provider: CompositeLocationProvider (9 location samples)
#  +	WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'larden', 3 location samples)
#  +	LogsLocationProvider (source: ../data/logs/larden.log, 6 location samples)
# [Suspect] Name: Hildegarde Schmidt, Location provider: CompositeLocationProvider (15 location samples)
#  +	CompositeLocationProvider (13 location samples)
# 	 +	PictureLocationProvider (source: '../data/pics/hschmidt' (JPG,JPEG,jpg,jpeg), 10 location samples)
# 	 +	LogsLocationProvider (source: ../data/logs/hschmidt.log, 3 location samples)
#  +	WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'hschmidt', 2 location samples)
# [Suspect] Name: Natalia Dragomiroff, Location provider: CompositeLocationProvider (16 location samples)
#  +	CompositeLocationProvider (13 location samples)
# 	 +	PictureLocationProvider (source: '../data/pics/ndragomiroff' (JPG,JPEG,jpg,jpeg), 9 location samples)
# 	 +	LogsLocationProvider (source: ../data/logs/ndragomiroff.log, 4 location samples)
#  +	WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'ndragomiroff', 3 location samples)
# [Suspect] Name: Hector MacQueen, Location provider: CompositeLocationProvider (16 location samples)
#  +	PictureLocationProvider (source: '../data/pics/hmacqueen' (JPG,JPEG,jpg,jpeg), 11 location samples)
#  +	WifiLogsLocationProvider (source: '../data/db/wifi.db', user 'hmacqueen', 5 location samples)
