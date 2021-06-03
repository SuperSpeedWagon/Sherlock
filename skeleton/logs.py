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
import re
from datetime import datetime, timezone, timedelta


# TODO: Définir la classe PictureLocationProvider qui désigne des objets
#       LocationProvider obtenus à partir de logs.
class LogsLocationProvider(ListLocationProvider):
    # TODO: Implémenter le constructeur où l'on définit en attribut le nom du
    #       fichier de log et où l'on construit la liste de samples.
    def __init__(self, log_file: str):
        # L'attribut contenant le nom du fichier est privé et l'attribut
        # __samples est hérité de ListLocationProvider
        self.__file = log_file
        samples = []
        try:
            f = open(log_file)
            lines = f.readlines()
            for l in lines:
                line = l.strip('\n')
                if l.find("source: GPS") != -1:  # garder seulement les coordonnées GPS
                    t, lat, lng = LogsLocationProvider._extract_location_sample_from_log(line)
                    if not (t is None or lat is None or lng is None):
                        loc = LocationSample(t, Location(lat, lng))
                        samples += [(f.name, loc)]
        except FileNotFoundError as e:
            print("Impossible de trouver le fichier donné.")
        else:
            print("Erreur")
        super().__init__(samples)

        # r= re.match("a(b|c)d", "abd")
        # TODO: parcourir les logs et filtrer ceux qui contiennent des appels
        #       GPS valides (coordonnées + temps).
        #       Générer un sample pour chaque log valide et l'ajouter à une
        #       liste temporaire.
        #       Appeler ensuite super en passant cette liste temporaire pour
        #       définir l'attribut __samples

    # TODO: Implémenter la méthode __str__ pour afficher les objets de la forme
    #       suivante.
    def __str__(self):
        return "LogsLocationProvider (" + self.__file + ", " + str(len(self.get_location_samples())) + " location samples)"

    # LogsLocationProvider (source: ../data/logs/jdoe.log, 2 location samples)

    # TODO: Implémenter la méthode _extract_location_sample_from_picture
    @staticmethod
    def _extract_location_sample_from_log(log: str):
        """
        Returns the time, latitude, and longitude, if available, from a given
        log.

        Returns
        -------
            The extracted time, latitude, and longitude.
        """

        (t, lat, lng) = (None, None, None)

        start = log.find("[")
        end = log.find("]")
        date_line = log[start+1:end]
        # gérer les UNKNOWNS
        t = datetime.strptime(date_line, "%Y-%m-%dT%H:%M:%S.%f")
        print(date_line)
        # remove [] substring
        line = log.split("]")[1]
        pair = re.findall(r"[-+]?\d*\.\d+|\d+", line)
        if not len(pair) == 0:
            print(pair)
            lat = float(pair[0])
            lng = float(pair[1])

        return t, lat, lng


if __name__ == '__main__':
    pass
    # Tester l'implémentation de cette classe avec les instructions de ce bloc
    # main (le résultat attendu est affiché ci-dessous).

    lp = LogsLocationProvider('../data/logs/hschmidt.log')
    print(lp)
    print(lp.get_surrounding_temporal_location_samples(datetime.strptime('2021-04-08 09:16:23', '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone(timedelta(hours=2)))))
    lp.show_location_samples()
    lp.print_location_samples()

    ### Résultat attendu ###

    # LogsLocationProvider (source: ../data/logs/hschmidt.log, 3 location samples)
    # LocationSample [datetime: 2021-04-08 09:16:21+02:00, location: Location [latitude: 46.52334, longitude: 6.57551]]
    # LocationSample [datetime: 2021-04-08 09:23:04+02:00, location: Location [latitude: 46.52475, longitude: 6.58057]]
    # LocationSample [datetime: 2021-04-08 09:27:18+02:00, location: Location [latitude: 46.52199, longitude: 6.58423]]
