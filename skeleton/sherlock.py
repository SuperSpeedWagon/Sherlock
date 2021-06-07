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

import argparse
from datetime import datetime, timedelta, timezone
from suspects import *
from configuration import *

DESCRIPTION = (
    "Identifie les suspects les plus plausibles à partir de leurs traces de "
    "mobilité (issues de sources multiples incluant les tweets géo-taggés, "
    "les traces Wi-Fi et les flux de photos géo-taggées) pour un crime spécifié "
    "par une date/heure et une localisation"
)

help_msg = ("usage : sherlock.py [−h] [−v] −s SUSPECT −t TWITTER_API_KEY\n" +
            utils.indent("−u TWITTER_API_KEY_SECRET −g GOOGLE_API_KEY −lat LATITUDE\n") +
            "−lng LONGITUDE −d DATE" + "\n" + DESCRIPTION + "\n" +
            "optional arguments :"
            "−h , −−help        show this help message and exit"
            "'−v , −−verbose affiche les details de l'execution du programme et les avertissements"
            "−s SUSPECT, −−suspect SUSPECT"
            "fichier contenant la liste des suspect.e.s et les sources de donnees de localisation (XML ou JSON )"
            "−t TWITTER_API_KEY , −−twitter−api−key TWITTER_API_KEY"
            "cle pour l'acces a l'API Twitter (cle privee de l'application Twitter)"
            "−u TWITTER_API_KEY SECRET , −−twitter−api−key−secret TWITTER_API_KEY_SECRET"
            "cle secrete pour l'acces a l'API Twitter"
            "−g GOOGLE_API_KEY, −−google−api−key GOOGLE_API_KEY"
            "cle pour l'acces a l'API Google (cle privee du compte developpeur Google)"
            "−lat LATITUDE, −−latitude LATITUDE"
            "latitude de la scene du crime"
            "−lng LONGITUDE, −−longitude LONGITUDE longitude de la scene du crime"
            "−d DATE, −−date DATE date et heure du crime (au format JJ/MM/AAAA−hh :mm :ss, par exemple 01/04/2019-17 "
            ":30 :20)")

if __name__ == "__main__":
    try:

        print(DESCRIPTION)
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument("-h", "--help", help="help", required=False, action="store_true")
        parser.add_argument("-v", "--verbose", help="verbose", required=False, action="store_true")
        parser.add_argument("-s", "--suspect", help="xml", required=True, type=str)
        parser.add_argument("-t", "--twitter-api-key", help="twitter_api_key", required=True, type=str)
        parser.add_argument("-u", "--twitter-api-key-secret", help="twitter_api_key_secret", required=True, type=str)
        parser.add_argument("-g", "--google-api-key", help="google_api_key", required=True, type=str)
        parser.add_argument("-lat", "--latitude", help="latitude", required=True, type=float)
        parser.add_argument("-lng", "--longitude", help="longitude", required=True, type=float)
        parser.add_argument("-d", "--date", help="date", required=True, type=str)

        args = parser.parse_args()

        conf = Configuration.get_instance()

        if args.help:
            print(help_msg)
            exit(Exception)

        if args.verbose:
            conf.add_element('verbose', True)
        else:
            conf.add_element('verbose', False)

        # twitter keys
        TwitterLocationProvider.set_api_key(args.twitter_api_key)
        TwitterLocationProvider.set_api_key_secret(args.twitter_api_key_secret)

        # google api key
        Location.set_api_key(args.google_api_key)

        conf.add_element("timezone", timezone(timedelta(hours=2)))
        conf.get_instance().add_element("crime_date",
                                        datetime.strptime(args.date, "%d/%m/%Y-%H :%M :%S").replace(
                                            conf.get_element("timezone")))
        conf.add_element("crime_location", Location(46.522874, 6.577165))
        crime = LocationSample(conf.get_element("crime_date"), conf.get_element("crime_location"))

        # TODO use google maps “ Investigation liee au crime du 06/05/2020 a 10:22:23 @ Banane, 1015 Ecublens, Suisse (46.5219,6.5791) ` ”
        api_file = open("apikey.txt", "r")
        api_key = api_file.read()
        api_file.close
        Location.set_api_key(api_key)
        print("Investigation liee au crime du {date:}" \
            " à {time:} @ {place:} ({lat:.4f}, {lng:.4f})".format(
                date=datetime.strftime(crime.get_date(), "%d/%m/%Y"), 
                time=datetime.strftime(crime.get_date(), "%H:%M:%S"),
                place=crime.get_location().get_name(),
                lat=crime.get_location().get_latitude(),
                lng=crime.get_location().get_longitude()
            )
        )
        
        suspects = Suspect.create_suspects_from_XML_file(args.suspect)
        suspect_array = []
        for s in suspects:
            if LocationProvider.could_have_been_there(s.get_location_provider()):
                suspect_array.append(s)

    except Exception:
        print("[Erreur] L'erreur suivante est survenue durant l'execution du programme: ...")



# manage exception
