#----------------------------------------------
# Code modified from courses.py in PA3
#----------------------------------------------

from math import radians, cos, sin, asin, sqrt
import sqlite3
import json
import re
import os


# Use this filename for the database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'improvements.db')

GAS_PRICE = 0.2808

def db_query(database, query):
    '''
    Given a database and a query, function connects to database, makes query,
    and returns the result.

    Inputs:
        database: database filename
        query: dictionary

    Returns:
        list
    '''
    db = sqlite3.connect(database)
    c = db.cursor()

    string = "SELECT btu_per_hour \
        FROM therms_improvements \
        WHERE device = ?"
    
    args = []
    args.append(query['device'])

    r = c.execute(string, args)

    result = r.fetchall()

    db.close()

    return result

def money_saved(args_from_ui):
    '''
    Takes a dictionary containing search criteria and returns courses
    that match the criteria.  The dictionary will contain some of the
    following fields:

      - dept a string
      - day is array with variable number of elements  
           -> ["'MWF'", "'TR'", etc.]
      - time_start is an integer in the range 0-2359
      - time_end is an integer an integer in the range 0-2359
      - enroll is an integer
      - walking_time is an integer
      - building ia string
      - terms is a string: "quantum plato"]

    Returns a pair: list of attribute names in order and a list
    containing query results.
    '''
    rv = []
    attr = ['money_saved_per_month']
    print(db_query(DATABASE_FILENAME, args_from_ui))
    btu = db_query(DATABASE_FILENAME, args_from_ui)[0][0]

    hours = query['hours_a_day']

    results = [("{0:.2f}".format(GAS_PRICE*hours*30.5*btu*(1/100000)),)]

    rv.append(attr)

    rv.append(results)
    return rv


def get_header(cursor):
    '''
    Given a cursor object, returns the appropriate header (column names)
    '''
    desc = cursor.description
    header = ()

    for i in desc:
        header = header + (clean_header(i[0]),)

    return list(header)


def clean_header(s):
    '''
    Removes table name from header
    '''
    for i in range(len(s)):
        if s[i] == ".":
            s = s[i+1:]
            break

    return s

# ########### some sample inputs #################
query = {"device": "Range-Oven Unit",
             "hours_a_day": 0.5}