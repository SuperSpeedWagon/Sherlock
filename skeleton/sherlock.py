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

if __name__ == "__main__":
    # try:
    if sys.argv == 1 and sys.argv[0] == '-h':
        print('')

    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument("-h", "--help", help="help", required=False, action="store_true")
    parser.add_argument("-v", "--verbose", help="verbose", required=False, action="store_true")
    parser.add_argument("-s", "--suspect", help="xml", required=True, type=str)
    parser.add_argument("-t", "--twitter-api-key", help="twitter_api_key", required=True, type=str)
    parser.add_argument("-u", "--twitter-api-key-secret", help="twitter_api_key_secret", required=True, type=str)
    parser.add_argument("-g", "--google-api-key", help="google_api_key", required=True, type=str)
    parser.add_argument("-lat", "--latitude", help="latitude", required=True, type=float)
    parser.add_argument("-lng", "--longitude", help="longitude", required=True, type=float)
    parser.add_argument("-d", "--date", help="date", required=True, type=datetime)

    # TODO: Ajouter les différents arguments de la ligne de commande à
    #       l'analyseur "parser".

    args = parser.parse_args()

    conf = Configuration.get_instance()

    if args.verbose:
        conf.add_element('verbose', True)
    else:
        conf.add_element('verbose', False)


    # TODO: Stocker les paramètres importants dans un objet Configuration
    #       accessible depuis tous les modules du programme.

    # TODO: Afficher le message d'accueil du logiciel.
    print(DESCRIPTION)

    # TODO: Lire le fichier suspect, l'analyser, construire les objets Suspect
    #       correspondants et les stocker dans une liste. Utiliser les méthodes
    #       createObjectFromXMLFile() / createObjectFromJSONFile().
    suspects = Suspect.create_suspects_from_XML_file(args.suspect)

    # TODO: Pour chaque suspect, déterminer s'il a pu se rendre et repartir du
    #       lieu du crime.
    #for s in suspects:

