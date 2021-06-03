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


def indent(text, space="\t"):
    new_line = "\n"
    lines = text.split(new_line)
    res = map(lambda line: space + line, lines)
    res = new_line.join(res)
    return res


def dict_factory(cursor, row):
    # Source: https://docs.python.org/3.6/library/sqlite3.html#sqlite3.Connection.row_factory
    # Dictionary factory to be used as a row_factory for SQL connection
    # It enables the use of query results as dictionaries, e.g.,
    # r = con.execute("SELECT age FROM ...).fetchone()"
    # age=r["age"]
    return dict([(col[0], row[idx]) for idx, col in enumerate(cursor.description)])


def get_if_exists(data, key, default=None):
    return data[key] if key in data else default


def filter_samples(samples, crime):
    # keep only samples from the day of the crime
    return [sample for sample in samples
            if sample.get_date().date() == crime.get_date().date()]


def convert_to_degrees(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF tags to
    degrees in float format.

    Parameters
    ----------
    value : exifread.classes.IfdTag

    Returns
    -------
    float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


if __name__ == '__main__':
    print("zero\n" + indent("one\n" + indent("two\nthree", "\t-")))
