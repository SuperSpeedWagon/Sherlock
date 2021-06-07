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

from datetime import datetime, timedelta, timezone
from abc import ABC, abstractmethod
import math
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
import folium
import googlemaps
import os
from configuration import *
import tempfile
import pathlib
import copy
import pprint
import calendar


class Location:
    __api_key = None
    __api_client = None

    @classmethod
    def set_api_key(cls, api_key: str):
        cls.__api_key = api_key
        cls.__api_client = googlemaps.Client(key=api_key)

    def __check_api_init(self):
        unil = (46.522313, 6.573909)
        epfl = (46.5185767, 6.5656641)
        success = False
        try:
            api_connect = self.__api_client.directions(
                unil,
                epfl,
                language="en",
                units="metric",
                mode="walking"
            )
            if (api_connect): success = True
        except Exception as error:
            print(error)
        return success

    def __init__(self, latitude: float, longitude: float):
        if (not (-180 < longitude < 180) or
                not (-180 < latitude < 180)):
            raise ValueError("longitude and latitude must be in range [-180, 180]")
        self._longitude = longitude
        self._latitude = latitude

    def __str__(self):
        return "Location [latitude: {lat:.5f}, longitude: {lon:.5f}]".format(lat=self._latitude, lon=self._longitude)

    def get_latitude(self):
        return self._latitude

    def get_longitude(self):
        return self._longitude

    def get_name(self):
        response = self.__api_client.reverse_geocode(
            (
                self._latitude,
                self._longitude
            ),
            language="fr"
        )
        address_name = response[0]["formatted_address"]

        return address_name

    def get_travel_distance_and_time(self, destination, mode="walking"):
        coord_orig = (self._latitude, self._longitude)
        coord_dest = (destination.get_latitude(), destination.get_longitude())
        response = self.__api_client.directions(
            coord_orig,
            coord_dest,
            language="en",
            units="metric",
            mode=mode
        )
        # pprint.pprint(response)

        legs = response[0]["legs"][0]
        travel_dist = legs["distance"]["value"]
        travel_time = legs["duration"]["value"]
        travel_time = timedelta(seconds=travel_time)

        return travel_dist, travel_time

    def __eq__(self, other):
        if not isinstance(other, Location):
            raise ValueError("illegal argument type. class Location expected")
        return self._longitude == other.get_longitude() and self._latitude == other.get_latitude()

    def __ne__(self, other):
        if not isinstance(other, Location):
            raise ValueError("illegal argument type. class Location expected")
        return self._longitude != other.get_longitude() or self._latitude != other.get_latitude()


class LocationSample:

    def __init__(self, date: datetime, location: Location, text: str = ""):
        lon = location.get_longitude()
        lat = location.get_latitude()
        self._location = Location(lat, lon)
        self._date = date .replace(tzinfo=timezone(timedelta(hours=2)))

    def get_location(self):
        return self._location

    def get_date(self):
        return self._date

    def get_description(self):
        position = "({lat:.2f}, {lng:.2f})" \
            .format(
            lat=self._location.get_latitude(),
            lng=self._location.get_longitude()
        )
        date = self._date.strftime("%Y-%m-%d, %H:%M:%S")
        return "<div>" \
               "<p>{str_date:<20}:{date:>20}</p>" \
               "<p>{str_position:<20}:{position:>20}</p>" \
               "</div>".format(
            str_date="date", date=date,
            str_position="coord", position=position
        )

    def __str__(self):
        return "LocationSample [" \
               "datetime: {date:}, " \
               "location: Location [" \
               "latitude: {lat:.5f}, " \
               "longitude: {lon:.5f}" \
               "]" \
               "]".format(
            date=str(self._date),
            lat=self._location.get_latitude(),
            lon=self._location.get_longitude()
        )

    def __eq__(self, other):
        if not isinstance(other, LocationSample):
            raise ValueError("illegal argument type. class LocationSample expected")
        return self._location == other.get_location() and self._date == other.get_date()

    def __ne__(self, other):
        if not isinstance(other, LocationSample):
            raise ValueError("illegal argument type. class LocationSample expected")
        return self._location != other.get_location() or self._date != other.get_date()

    def __ge__(self, other):
        if not isinstance(other, LocationSample):
            raise ValueError("illegal argument type. class LocationSample expected")
        else:
            return self._date >= other.get_date()

    def __gt__(self, other):
        if not isinstance(other, LocationSample):
            raise ValueError("illegal argument type. class LocationSample expected")
        else:
            return self._date > other.get_date()

    def __le__(self, other):
        if not isinstance(other, LocationSample):
            raise ValueError("illegal argument type. class LocationSample expected")
        else:
            return self._date <= other.get_date()

    def __lt__(self, other):
        if not isinstance(other, LocationSample):
            raise ValueError("illegal argument type. class LocationSample expected")
        else:
            return self._date < other.get_date()


class LocationProvider:
    app = None
    web = None

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_location_samples(self):
        pass

    def print_location_samples(self):
        for s in self.get_location_samples():
            print(s)

    def show_location_samples(self, marker: LocationSample = None, showPath=False, title=None):
        self.__class__.app = QApplication.instance()
        if self.__class__.app is None:
            self.__class__.app = QApplication([''])
        self.__class__.web = QWebEngineView()

        samples = self.get_location_samples()
        if len(samples) == 0:
            return

        coordinates = [(sample.get_location().get_latitude(), sample.get_location().get_longitude()) for sample in
                       samples]
        timestamps = [sample.get_date() for sample in samples]
        try:
            data = [sample.get_description() for sample in samples]
        except NotImplementedError:  # if get_description is not implemented yet
            data = ["" for _ in samples]

        # Creating the html map, zoom in location defined by the first coordinate
        map_ = folium.Map(location=coordinates[0], zoom_start=15, detect_retina=False,
                          API_key='pk.eyJ1IjoiaXNwbGFiLXVuaWwiLCJhIjoiY2oxeGl4eTFuMDAwYTJxbzB0bXg1dmxzcCJ9.d14dldYH5NpracBPF3X4pg',
                          tiles='https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiaXNwbGFiLXVuaWwiLCJhIjoiY2oxeGl4eTFuMDAwYTJxbzB0bXg1dmxzcCJ9.d14dldYH5NpracBPF3X4pg',
                          attr='Mapbox')

        folium.PolyLine(locations=coordinates).add_to(map_)  # draw a line connecting all the points

        for i in range(0, len(coordinates)):
            popup = folium.Popup(folium.Html(
                f"<strong>{timestamps[i].strftime('%Y-%m-%d at %I:%M:%S%p %Z')}</strong></br> Source: {data[i]}",
                script=True))
            folium.Marker(coordinates[i], popup=popup).add_to(map_)  # put markers on each and annotate with timestamps

        if marker is not None:
            coordinate = (marker.get_location().get_latitude(), marker.get_location().get_longitude())
            popup = folium.Popup(folium.Html(
                f"<strong>{marker.get_date().strftime('%Y-%m-%d at %I:%M:%S%p %Z')}</strong></br>"
                f"{marker.get_description()}", script=True))
            folium.Marker(coordinate, popup=popup, icon=folium.Icon(color='red')).add_to(map_)
            coordinates.append(coordinate)

            if showPath:
                # get LocationSamples right before and right after
                (ls_before, ls_after) = self.get_surrounding_temporal_location_samples(marker.get_date())

                # determine the compatibility based on the time needed and the actual time (elapsed)
                if ls_before:
                    dt_before_actual = marker.get_date() - ls_before.get_date()
                    _, dt_before_needed = ls_before.get_location().get_travel_distance_and_time(marker.get_location())
                    popup = folium.Popup(folium.Html(
                        f'Temps {"vers"} le lieu du crime :</br><ul style="margin-left:-2em;"><li>Réel : '
                        f'{dt_before_actual}</li><li>Google Maps : {dt_before_needed}</li></ul>', script=True))

                    folium.PolyLine(popup=popup,
                                    locations=[
                                        (sample.get_location().get_latitude(), sample.get_location().get_longitude())
                                        for sample in [ls_before, marker]], color='red', weight=2).add_to(map_)

                if ls_after:
                    dt_after_actual = ls_after.get_date() - marker.get_date()
                    _, dt_after_needed = marker.get_location().get_travel_distance_and_time(ls_after.get_location())
                    popup = folium.Popup(folium.Html(
                        f'Temps {"vers"} le lieu du crime :</br><ul style="margin-left:-2em;"><li>Réel : '
                        f'{dt_after_actual}</li><li>Google Maps : {dt_after_needed}</li></ul>', script=True))

                    folium.PolyLine(popup=popup,
                                    locations=[
                                        (sample.get_location().get_latitude(), sample.get_location().get_longitude())
                                        for sample in [ls_after, marker]], color='red', weight=2).add_to(map_)

        map_.fit_bounds(coordinates)

        # path = os.path.abspath('./map.html')
        (_, path) = tempfile.mkstemp(prefix='sherlock_', suffix='_map.html')
        try:
            if Configuration.get_instance().get_element("verbose", False):
                print(f"Creating temporary file for the map to be displayed '{path}'", file=sys.stderr)
        except NotImplementedError:
            print(f"Creating temporary file for the map to be displayed '{path}'", file=sys.stderr)
        map_.save(path)
        url = pathlib.Path(os.path.abspath(path)).as_uri()

        self.__class__.web.setWindowTitle(f'Trace de mobilité {f"({title})" if title is not None else ""}')
        self.__class__.web.load(QUrl(url))
        self.__class__.web.show()
        status = self.__class__.app.exec()

        if status != 0 and Configuration.get_instance().get_element("verbose", False):
            print(f'Warning: The QApplication displaying the web-based map finished with exit code {status}',
                  file=sys.stderr)

        try:
            os.unlink(path)
        except Exception as e:
            if Configuration.get_instance().get_element("verbose", False):
                print(f'Warning: An error has occurred while removing a temporary file ({e})',
                      file=sys.stderr)

    def get_surrounding_temporal_location_samples(self, timestamp: datetime):
        #timestamp = calendar.timegm(timestamp.timetuple())
        samples = self.get_location_samples()
        prev = next_ = None

        for i in range(len(samples)):
            curr_date = samples[i].get_date()
            if i == 0 and curr_date > timestamp:
                next_ = samples[i]
                break
            elif i > 0 and curr_date > timestamp:
                next_ = samples[i]
                prev = samples[i - 1]
                break
        if len(samples) and not next_:
            prev = samples[-1]
        return prev, next_

    def could_have_been_there(self, ls: LocationSample):
        crime = ls
        a, b = self.get_surrounding_temporal_location_samples(crime.get_date())
        # suspect inferred travel time (from A to B through Crime)
        tto_crime = (crime.get_date() - a.get_date()).total_seconds()
        tfrom_crime = (b.get_date() - crime.get_date()).total_seconds()
        inferred_time = tto_crime + tfrom_crime
        # theoretical travel time (from A to B)
        _, theoretical_time = a.get_location().get_travel_distance_and_time(b.get_location())

        return theoretical_time >= inferred_time

    def __str__(self):
        n = len(self.get_location_samples())
        return "LocationProvider ({:d} location samples)".format(n)

    def __add__(self, other):
        return CompositeLocationProvider(self, other)


class ListLocationProvider(LocationProvider):

    def __init__(self, list_location_sample):
        # self.__location_samples = copy.deepcopy(list_location_sample)
        self.__location_samples = []
        for ls in list_location_sample:
            self.__location_samples += [copy.deepcopy(ls)]

    def get_location_samples(self):
        return self.__location_samples


class CompositeLocationProvider(LocationProvider):

    def __init__(self, lp1: LocationProvider, lp2: LocationProvider):
        self.__lp1 = lp1
        self.__lp2 = lp2

    def get_location_samples(self):
        return self.__lp1.get_location_samples() + self.__lp2.get_location_samples()

    def __str__(self):
        return "CompositeLocationProvider (" + str(
            len(self.__lp1.get_location_samples()) + len(
                self.__lp2.get_location_samples())) + " location samples)\n" + " +" + utils.indent(
            str(self.__lp1)) + "\n +" + utils.indent(str(self.__lp2))


# CompositeLocationProvider (4 location samples)
#  +	ListLocationProvider (2 location samples)
#  +	ListLocationProvider (2 location samples)

if __name__ == '__main__':
    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)
    Configuration.get_instance().add_element("verbose", True)
    Location.set_api_key('AIzaSyAtMl3hOMtmLuUYk-bDPdVThgIEwBKDG7o')

    # ---------------- API key --------------------
    #api_file = open("apikey.txt", "r")
    #api_key = api_file.read()
    #api_file.close
    #Location.set_api_key(api_key)
    # ---------------------------------------------

    paris = Location(48.854788, 2.347557)
    lausanne = Location(46.517738, 6.632233)
    print(lausanne.get_name())

    sample1 = LocationSample(datetime(2019, 3, 3, 12, 25), paris)
    print(sample1.get_location())
    print(sample1.get_date())
    print(sample1)

    sample2 = LocationSample(datetime(2019, 3, 3, 14, 56, 5), lausanne)
    print(sample1 < sample2)

    a = [sample2, sample1]
    a.sort()

    print([str(x) for x in a])

    crime = LocationSample(datetime(2019, 3, 31, 18, 30, 20), Location(46.520336, 6.572844))
    print(crime.get_location().get_travel_distance_and_time(Location(46.521045, 6.574664)))

    locationsamples = ListLocationProvider([sample1, sample2])
    print(locationsamples.get_location_samples())
    locationsamples.show_location_samples()

    # print(locationsamples + locationsamples)

    ### Résultat attendu ###

    # Avenue Sainte-Luce 8, 1003 Lausanne, Suisse
    # Location [latitude: 48.85479, longitude: 2.34756]
    # 2019-03-03 12:25:00
    # LocationSample [datetime: 2019-03-03 12:25:00, location: Location [latitude: 48.85479, longitude: 2.34756]]
    # True
    # ['LocationSample [datetime: 2019-03-03 12:25:00, location: Location [latitude: 48.85479, longitude: 2.34756]]', 'LocationSample [datetime: 2019-03-03 14:56:05, location: Location [latitude: 46.51774, longitude: 6.63223]]']
    # (179, datetime.timedelta(seconds=129))
    # [LocationSample [datetime: 2019-03-03 12:25:00, location: Location [latitude: 48.85479, longitude: 2.34756]], LocationSample [datetime: 2019-03-03 14:56:05, location: Location [latitude: 46.51774, longitude: 6.63223]]]
    # CompositeLocationProvider (4 location samples)
    #  +	ListLocationProvider (2 location samples)
    #  +	ListLocationProvider (2 location samples)
