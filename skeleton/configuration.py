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

import utils


# TODO: Créer une classe Configuration contenant:
#       - une structure de données adéquate pour stocker des couples
#         clefs-valeurs pour les paramètres de configuration
#       - une méthode add_element pour ajouter un nouvel élément
#       - une méthode get_element pour récupérer la valeur d'un paramètre à
#         partir de sa clef

# TODO: Utiliser le patron de conception Singleton pour cette classe, pour
#       manipuler la configuration de manière globale dans tout le programme.


class Configuration:

    __instance = None

    def __init__(self):
        self.__class__.__instance = self
        self.__dict = {}

    def __str__(self):
        return str(self.__dict)

    def add_element(self, key, value):
        self.__dict[key] = value

    def get_element(self, key, default=None):
        return self.__dict.get(key, default)

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            Configuration()
        return cls.__instance


if __name__ == '__main__':
    conf = Configuration.get_instance()

    conf.add_element('verbose', True)
    conf.add_element('N', 6)
    print(conf)

    max = conf.get_element('max', 42)
    print(max, conf.get_element('nax'), conf.get_element('verbose'))

    print(conf == Configuration.get_instance())

### Résultat attendu ###

# {'verbose': True, 'N': 6}
# 42 None True
# True
