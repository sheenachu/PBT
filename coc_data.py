# Reads and organizes the City of Chicago data.
#
# Created by Kevin Bernat
#

import csv
import coords_to_block
import numpy as np

def read_csv(filename):
    """
    Reads a csv file and stores the information into a list.
    """
    l = []

    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, quotechar='|')
        for row in spamreader:
            l.append(row)
    return l

def neighborhood(l):
    """
    LEGACY CODE.
    """
    d = {}
    n = 0
    for row in l[1:]:
        neighborhood = row[0]

        if neighborhood not in d:

            d[neighborhood] = [{n:row[1:]}]
        else:
            d[neighborhood].append({n:row[1:]})    
        n += 1

    return d 
  
def building_list(l):
    """
    LEGACY CODE -- Not used in project

    Creates a list of the buildings in the City of Chicago data.
    They are ordered by as follows:
    {census_block:{building_type:{building_subtype:list of other information}}}
    """

    building_dict ={}

    for row in l[1:]:
        if row[1] != '' and row[2] != '' and row[3] != '':
            census_block = row[1]

            building_type = row[2]
            building_subtype = row[3]

            if census_block not in building_dict:
                building_dict[census_block] = [{building_type:{building_subtype:[row[0]] + row[4:]}}]
            else:
                building_dict[census_block].append({building_type:{building_subtype:[row[0]] + row[4:]}})

    return building_dict

def neighborhood_totals(l):
    """
    Loops through the list of buildings and finds the items that
    correspond to neighborhood totals and stores this information
    into a dictionary.
    """
    d = {}
    for row in l[1:]:
        if row[1] == '' and row[2] == '' and row[3] == '':
            d[row[0]] = row[4:]
    return d               

def find_building(building_dict, address, building_type, building_subtype):
    """
    LEGACY CODE -- Not used in final project
    Given an address, building type, and building subtype,
    the appropriate row from the City of Chicago data is selected.
    """

    coords = coords_to_block.addr_to_coords(coords_to_block.address_url, address)   
    census_block = coords_to_block.visit_pages(coords_to_block.url,coords)

    matches = building_dict[str(census_block)]

    for match in matches:
        print(match)

        for key in match.keys():
            print(key)
            print(key == building_type)
            if key == building_type:
                value = match[key]
                print(value) 
                for key2 in value.keys():
                    if key2 == building_subtype:
                        ans = match[building_type][building_subtype]
                    else:
                        break

    return ans

def census_block_data(l, filename):
    """
    Modifies the City of Chicago data such that it aggregates
    the information based on the census blocks. 

    Returns a dictionary with the electricity/gas usage in each
    census block.

    """

    d = {}
    for row in l[1:]:
        if '' in row:
            pass
        else:     
            row[4:17] = [float(i) for i in row[4:17]]
            row[4:17] = list(map(float, row[4:17])) #http://stackoverflow.com/questions/7368789/convert-all-strings-in-a-list-to-int
            if row[19] == '' or row[18] == '':
                 pass
            else:
                row[19] = float(row[19])
                row[18] = float(row[18])
                if row[1] not in d:
                    if filename == "Energy_Usage_2010_elec.csv":
                        values = np.array(row[4:17] + [row[19]])
                    if filename == "Energy_Usage_2010_therms.csv":
                        values = np.array(row[4:17] + [row[18]]) 

                    d[row[1]] = values

                else:
                    if filename == "Energy_Usage_2010_elec.csv":
                        values = np.array(row[4:17] + [0])
                    if filename == "Energy_Usage_2010_therms.csv":
                        values = np.array(row[4:17] + [0])

                    values = values + d[row[1]]

                    d[row[1]] = values 

    return d  

def census_csv(census_block_dict,filename):
    """
    Creates a csv with electricity or gas usage organized 
    based on each census block.
    """
     with open(filename, "wt") as result:
        writer = csv.writer(result)
        writer.writerow(("census","jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec","tot","population"))
        for key in census_block_dict.keys():
            writer.writerow((key, census_block_dict[key][0], census_block_dict[key][1],
                census_block_dict[key][2],census_block_dict[key][3],census_block_dict[key][4],
                census_block_dict[key][5],census_block_dict[key][6],census_block_dict[key][7],
                census_block_dict[key][8],census_block_dict[key][9],census_block_dict[key][10],
                census_block_dict[key][11],census_block_dict[key][12],census_block_dict[key][13]))

