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

ATTRIBUTES = ["device", "hours_a_day", "btu_per_hour",
            "therms_saved_per_month", "money_saved_per_month"]

PARAMS_ATTRS = {"device" : ["money_saved_per_month"],
                "hours_a_day" : ["money_saved_per_month"],}

SCHEMA = {"device" : "hours_a_day": "btu_per_hour": "therms_saved_per_month", "money_saved_per_month"}

def select_list(query):
    '''
    Function takes a query and returns a list of strings to be passed to SELECT
    
    Inputs:
        query: dictionary
    
    Returns:
        list of strings
    '''
    attr = []
    rv = []
    for key in query:
        for attribute in PARAMS_ATTRS[key]:
            if attribute not in attr:
                attr.append(attribute)
    for value in ATTRIBUTES:
        if value in attr:
            if value in SCHEMA:
                rv.append(SCHEMA[value])
            else:
                rv.append(value)

    return rv

def attr_list(query):
    '''
    Function takes a query and returns a list of attributes

    Inputs:
        query: dictionary

    Returns:
        list of strings
    '''
    attr = []
    rv = []
    for key in query:
        for attribute in PARAMS_ATTRS[key]:
            if attribute not in attr:
                attr.append(attribute)
    for value in ATTRIBUTES:
        if value in attr:
                rv.append(value)

    return rv


def where_list(query):
    '''
    Function takes a query and returns a list of strings that will be passed
    to WHERE as well as an accompanying list of parameters

    Inputs:
        query: dictionary

    Returns:
        list of strings
        list of strings
    '''
    wheres = []
    args = []

    for key in query:
        boo = "="
        if key == "day":
            rd = []
            for d in query[key]:
                rd.append('{} {} ?'.format(SCHEMA[key], boo))
                args.append(d)
            rd = ' OR '.join(rd)
            wheres.append('({})'.format(rd))
            continue
        if key == "building":
            wheres.append("b.building_code = ?")
            args.append(query[key])
            continue

        if key == "walking_time":
            dist_string = "walking_time <= ?"
            wheres.append(dist_string)
            args.append(query[key])
            continue        
        if key == "terms":
            list_terms = []
            list_terms = query[key].split()
            rd = []
            for t in list_terms:
                rd.append('{} {} ?'.format(SCHEMA[key], boo))
                args.append(t)
            rd = ' OR '.join(rd)
            wheres.append('({})'.format(rd))
            continue
        if key in ["time_start", "enroll_lower"]:
            boo = ">="
        if key in ["time_end", "enroll_upper"]:
            boo = "<="
        wheres.append('{} {} ?'.format(SCHEMA[key], boo))
        args.append(str(query[key]))

    return wheres, args


def sql_string(query, s_list, w_list):
    '''
    Given a query, a list of SELECTS, and a list of WHEREs, function generates
    a SQL string.

    Inputs:
        query: dictionary
        s_list: list of strings
        w_list: list of strings

    Returns:
        string
    '''
    s_string = ", ".join(s_list)
    w_string = " AND ".join(w_list)

    string = "SELECT {}\
        FROM courses AS c \
        JOIN sections AS s ON c.course_id = s.course_id \
        JOIN meeting_patterns AS mp ON s.meeting_pattern_id = \
        mp.meeting_pattern_id".format(s_string)
        

    if "walking_time" in query.keys():
        string += " JOIN gps AS a ON a.building_code = s.building_code \
                    JOIN gps AS b"
    if "terms" in query.keys():
        list_terms = []
        list_terms = query['terms'].split()
        group_string = "GROUP BY c.course_num, s.section_num HAVING count(*) = "  + str(len(list_terms))

        string += " JOIN catalog_index AS ci ON c.course_id = ci.course_id"
        string += " WHERE {} {}".format(w_string, 
                    group_string)
    else:
        string += " WHERE {}".format(w_string)
    
    return string

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

    s_list = select_list(query)
    w_list, args = where_list(query)

    string = sql_string(query, s_list, w_list)

    args_string = ", ".format(args)

    db.create_function("time_between", 4, compute_time_between)
    r = c.execute(string, args)

    result = r.fetchall()

    db.close()

    return result

def find_courses(args_from_ui):
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
    attr = attr_list(args_from_ui)
    results = db_query(DATABASE_FILENAME, args_from_ui)
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

########### some sample inputs #################

example_0 = {"Device": "Bathtub",
             "Reduced Hours": 8}