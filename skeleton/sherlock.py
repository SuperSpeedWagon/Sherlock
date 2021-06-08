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

import utils
from suspects import *
from configuration import *

DESCRIPTION = (
    "Identifie les suspects les plus plausibles à partir de leurs traces de "
    "mobilité (issues de sources multiples incluant les tweets géo-taggés, "
    "les traces Wi-Fi et les flux de photos géo-taggées) pour un crime spécifié "
    "par une date/heure et une localisation"
)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description=DESCRIPTION, add_help=True)
        parser.add_argument("-v", "--verbose",
                            help="affiche les details de l'execution du programme et les avertissements",
                            required=False, action="store_true")
        parser.add_argument("-s", "--suspect",
                            help="fichier contenant la liste des suspect.e.s et les sources de donnees de localisation ("
                                 "XML ou JSON)",
                            required=True, type=str)
        parser.add_argument("-t", "--twitter-api-key",
                            help="clé pour l'acces a l'API Twitter (clé privee de l'application Twitter)",
                            required=True,
                            type=str)
        parser.add_argument("-u", "--twitter-api-key-secret", help="clé secrete pour l'acces a l'API Twitter",
                            required=True, type=str)
        parser.add_argument("-g", "--google-api-key",
                            help="clé pour l'acces a l'API Google (cle privee du compte developpeur Google)",
                            required=True,
                            type=str)
        parser.add_argument("-lat", "--latitude", help="latitude de la scene du crime", required=True, type=float)
        parser.add_argument("-lng", "--longitude", help="longitude de la scene du crime", required=True, type=float)
        parser.add_argument("-d", "--date",
                            help="date et heure du crime (au format JJ/MM/AAAA−hh:mm:ss, par exemple 01/04/2019-17:30:20)",
                            required=True, type=str)

        args = parser.parse_args()

        conf = Configuration.get_instance()
        parser = argparse.ArgumentParser(description=DESCRIPTION, add_help=True)
        parser.add_argument("-v", "--verbose", help="affiche les details de l'execution du programme et les avertissements",
                            required=False, action="store_true")
        parser.add_argument("-s", "--suspect",
                            help="fichier contenant la liste des suspect.e.s et les sources de donnees de localisation ("
                                 "XML ou JSON)",
                            required=True, type=str)
        parser.add_argument("-t", "--twitter-api-key",
                            help="clé pour l'acces a l'API Twitter (clé privee de l'application Twitter)", required=True,
                            type=str)
        parser.add_argument("-u", "--twitter-api-key-secret", help="clé secrete pour l'acces a l'API Twitter",
                            required=True, type=str)
        parser.add_argument("-g", "--google-api-key",
                            help="clé pour l'acces a l'API Google (cle privee du compte developpeur Google)", required=True,
                            type=str)
        parser.add_argument("-lat", "--latitude", help="latitude de la scene du crime", required=True, type=float)
        parser.add_argument("-lng", "--longitude", help="longitude de la scene du crime", required=True, type=float)
        parser.add_argument("-d", "--date",
                            help="date et heure du crime (au format JJ/MM/AAAA−hh:mm:ss, par exemple 01/04/2019-17:30:20)",
                            required=True, type=str)

        args = parser.parse_args()

        conf = Configuration.get_instance()

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
                                        datetime.strptime(args.date, "%d/%m/%Y-%H:%M:%S").replace(tzinfo=
                                        conf.get_element(
                                            "timezone")))
        conf.add_element("crime_location", Location(46.522874, 6.577165))
        crime = LocationSample(conf.get_element("crime_date"), conf.get_element("crime_location"))

        print("Investigation liee au crime du {date:}" \
              " à {time:} @ {place:} ({lat:.4f}, {lng:.4f})".format(
            date=datetime.strftime(crime.get_date(), "%d/%m/%Y"),
            time=datetime.strftime(crime.get_date(), "%H:%M:%S"),
            place=crime.get_location().get_name(),
            lat=crime.get_location().get_latitude(),
            lng=crime.get_location().get_longitude()
        )
        )
        samples = [crime]
        list1 = ListLocationProvider(samples)
        suspects = Suspect.create_suspects_from_XML_file(args.suspect)
        suspect_array = []
        for s in suspects:
            for l in s.get_location_provider().get_location_samples():
                if list1.could_have_been_there(l):
                    suspect_array.append(s)

        for s in suspect_array:
            print(s.get_name())

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
                                            datetime.strptime(args.date, "%d/%m/%Y-%H:%M:%S").replace(tzinfo=
                                            conf.get_element(
                                                "timezone")))
            conf.add_element("crime_location", Location(46.522874, 6.577165))
            crime = LocationSample(conf.get_element("crime_date"), conf.get_element("crime_location"))

            print("Investigation liee au crime du {date:}" \
                  " à {time:} @ {place:} ({lat:.4f}, {lng:.4f})".format(
                date=datetime.strftime(crime.get_date(), "%d/%m/%Y"),
                time=datetime.strftime(crime.get_date(), "%H:%M:%S"),
                place=crime.get_location().get_name(),
                lat=crime.get_location().get_latitude(),
                lng=crime.get_location().get_longitude()
            )
            )
            samples = [crime]
            list1 = ListLocationProvider(samples)
            suspects = Suspect.create_suspects_from_XML_file(args.suspect)
            suspect_array = []
            for s in suspects:
                for l in s.get_location_provider().get_location_samples():
                    if list1.could_have_been_there(l):
                        suspect_array.append(s)

            for s in suspect_array:
                print(s.get_name())

    except Exception:
        print("[Erreur] L'erreur suivante est survenue durant l'execution du programme: ...")
