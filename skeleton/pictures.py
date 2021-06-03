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

from abc import ABC

from location import *
from functools import reduce
import os
import utils
import sys
import time
import exifread
from datetime import datetime, timezone, timedelta


class PictureLocationProvider(ListLocationProvider):

    def __init__(self, directory: str):
        self._VALID_EXTENSIONS = [".JPG", ".JPEG", ".jpg", ".jpeg"]
        self.__dir = directory
        samples = []
        # samples doit contenir des couples (String: source_pic_file, LocationSample: sample)
        # de sorte à garder une trace de l'origine de chaque objet LocationSample
        for f in os.scandir(directory):
            valid = False
            for i in self.get_list_valid_extensions():
                if f.name.endswith(i):
                    valid = True
            if not valid:
                print("Attention: fichier ignoré ’" + f.name + "’ (Informations de temps et/ou location manquantes)")
            else:
                t, lat, lng = PictureLocationProvider._extract_location_sample_from_picture(f)
                if not (t is None or lat is None or lng is None):
                    loc = LocationSample(t, Location(lat, lng))
                    samples += [(f.name, loc)]
        super(PictureLocationProvider, self).__init__(samples)

    def get_directory(self):
        return self.__dir

    def get_list_valid_extensions(self):
        return copy.deepcopy(self._VALID_EXTENSIONS)

    # TODO: Redéfinir la méthode __str__ pour afficher les objets sous la forme
    #       suivante :
    def __str__(self):
        return "PictureLocationProvider (source: ’ " + str(self.get_directory()) + "’ (" + str(
            self.get_list_valid_extensions()) + "), " + str(
            len(super(PictureLocationProvider, self).get_location_samples())) + " location samples)"

    @staticmethod
    def _extract_location_sample_from_picture(filename: str):
        """
        Returns the time, latitude, and longitude, if available, from the EXIF
        data extracted from the file specified by filename.

        Parameters
        ----------
        filename

        Returns
        -------
        tuple
            Tuple containing the time, latitude, and longitude (if available)
            that was extracted from the EXIF tags of `filename`.
        """
        (t, lat, lng) = (None, None, None)

        with open(filename, 'rb') as f:
            exif_data = exifread.process_file(f)

            gps_latitude = utils.get_if_exists(exif_data, 'GPS GPSLatitude')
            gps_latitude_ref = utils.get_if_exists(exif_data, 'GPS GPSLatitudeRef')
            gps_longitude = utils.get_if_exists(exif_data, 'GPS GPSLongitude')
            gps_longitude_ref = utils.get_if_exists(exif_data, 'GPS GPSLongitudeRef')

            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = utils.convert_to_degrees(gps_latitude)
                if gps_latitude_ref.values[0] != 'N':
                    lat = -lat

                lng = utils.convert_to_degrees(gps_longitude)
                if gps_longitude_ref.values[0] != 'E':
                    lng = -lng

            date = utils.get_if_exists(exif_data, 'GPS GPSDate')
            timestamp = utils.get_if_exists(exif_data, 'GPS GPSTimeStamp')

            t = datetime.strptime(str(date), "%Y:%m:%d")

        return t, lat, lng


if __name__ == '__main__':
    # Tester l'implémentation de cette classe avec les instructions de ce bloc
    # main (le résultat attendu est affiché ci-dessous).

    Configuration.get_instance().add_element("verbose", True)
    lp = PictureLocationProvider('../data/pics/chardman')

    print(lp)
    lp.show_location_samples()

    ### Résultat attendu ###

    # PictureLocationProvider (source: '../data/pics/chardman' (JPG,JPEG,jpg,jpeg), 2 location samples)
