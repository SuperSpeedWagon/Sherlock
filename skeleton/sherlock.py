#!venv/bin/python3
# -*- coding: utf-8 -*-
__author__ = "Benjamin Trubert, Kévin Huguenin, Alpha Diallo, Lev Velykoivanenko, Noé Zufferey"
__copyright__ = "Copyright 2021, The Information Security and Privacy Lab at the University of Lausanne (" \
                "https://www.unil.ch/isplab/)"
__credits__ = ["Benjamin Trubert", "Kévin Huguenin", "Alpha Diallo", "Lev Velykoivanenko", "Noé Zufferey", "Vaibhav Kulkarni"]

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

    parser = argparse.ArgumentParser(description=DESCRIPTION)

    # TODO: Ajouter les différents arguments de la ligne de commande à
    #       l'analyseur "parser".

    args = parser.parse_args()

    # TODO: Stocker les paramètres importants dans un objet Configuration
    #       accessible depuis tous les modules du programme.

    # TODO: Afficher le message d'accueil du logiciel.

    # TODO: Lire le fichier suspect, l'analyser, construire les objets Suspect
    #       correspondants et les stocker dans une liste. Utiliser les méthodes
    #       createObjectFromXMLFile() / createObjectFromJSONFile().

    # TODO: Pour chaque suspect, déterminer s'il a pu se rendre et repartir du
    #       lieu du crime.
