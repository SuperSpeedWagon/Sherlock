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

from location import *
import tweepy
import sys
import time
from configuration import *
import html
from datetime import datetime, timezone, timedelta


class TwitterLocationProvider():
    __api_key = None
    __api_key_secret = None

    def __init__(self, twitter_username: str, twitter_access_token: str, twitter_access_token_secret: str):
        self.__twitter_username = twitter_username
        self.__twitter_access_token = twitter_access_token
        self.__twitter_access_token_secret = twitter_access_token_secret
        self.__list_location_sample = []

    def set_api_key(self, api_key: str):
        self.__api_key = api_key

    def set_api_key_secret(self, api_key: str):
        self.__api_key_secret = api_key

    def __str__(self):
        return "TwitterLocationProvider" \
               " (user '{username:s}'" \
               " aka '{black_magic:s}'," \
               " {n:d} location samples)".format(
            username=self.__twitter_username,
            black_magic="to be defined",
            n=len(self.__list_location_sample)
        )

    # TODO: Implémenter la méthode _extract_location_sample_from_tweet qui prend
    #       en paramètre un tweet et renvoie un tuple (temps, latitude, longitude).
    # Comme pour la méthode de Picture, vérifier que les paramètres sont bien présents dans le tweet
    def _extract_location_sample_from_tweet(self, tweet):
        latitude = tweet['coordinates']['latitude']
        longitude = tweet['coordinates']['longitude']
        time = None

        return time, latitude, longitude


if __name__ == '__main__':
    pass
    # Tester l'implémentation de cette classe avec les instructions de ce bloc
    # main (le résultat attendu est affiché ci-dessous).

    # Configuration.get_instance().add_element("verbose", True)
    # Configuration.get_instance().add_element("crime_date", datetime.strptime("08/04/2021", "%d/%m/%Y"))
    # TwitterLocationProvider.set_api_key('Z4bLkruoqSp0JXJfJGTaMQEZo')
    # TwitterLocationProvider.set_api_key_secret('gYyLCa7QiDje76VaTttlylDjGThCBGcp9MIcEGlzVq6FJcXIdc')
    #
    # lp = TwitterLocationProvider('rvkint95', '842358721544101888-AMqXbdV1ciZ6XIpcmfKDwMeadzxwBHb', '8ptgdczduqQVIrpVh7aXrmOdp8MDDLaUvThwP3bRfyk9g')
    #
    # print(lp)
    # lp.print_location_samples()
    # lp.show_location_samples()

    ### Résultat attendu ###

    # TwitterLocationProvider (user 'rvkint95' aka 'Verbal', 10 location samples)
    # LocationSample [datetime: 2021-04-08 07:10:40+00:00, location: Location [latitude: 46.51998, longitude: 6.57425]]
    # LocationSample [datetime: 2021-04-08 07:12:46+00:00, location: Location [latitude: 46.52105, longitude: 6.57478]]
    # LocationSample [datetime: 2021-04-08 07:14:02+00:00, location: Location [latitude: 46.52119, longitude: 6.57618]]
    # LocationSample [datetime: 2021-04-08 07:16:57+00:00, location: Location [latitude: 46.52157, longitude: 6.57791]]
    # LocationSample [datetime: 2021-04-08 07:17:43+00:00, location: Location [latitude: 46.52058, longitude: 6.57817]]
    # LocationSample [datetime: 2021-04-08 07:19:03+00:00, location: Location [latitude: 46.51991, longitude: 6.57785]]
    # LocationSample [datetime: 2021-04-08 07:21:52+00:00, location: Location [latitude: 46.52031, longitude: 6.58043]]
    # LocationSample [datetime: 2021-04-08 07:22:43+00:00, location: Location [latitude: 46.52063, longitude: 6.58199]]
    # LocationSample [datetime: 2021-04-08 07:24:33+00:00, location: Location [latitude: 46.52172, longitude: 6.58186]]
    # LocationSample [datetime: 2021-04-08 07:27:05+00:00, location: Location [latitude: 46.52164, longitude: 6.58351]]
