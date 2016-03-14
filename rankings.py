# Purpose: Determine the ranking of the different neighborhoods
# in Chicago
#
# Created by Kevin Bernat
#

import coc_data
import quicksort
import csv

l_elec = coc_data.read_csv("Energy_Usage_2010_elec.csv")
gas = coc_data.read_csv("Energy_Usage_2010_therms.csv")
month_dict = {"jan":0, "feb":1, "mar":2, "apr":3, "may":4,
"jun":5,"jul":6,"aug":7,"sep":8,"oct":9,"nov":10,"dec":11,"tot":12}

def determine_ranking(l,month):
    """
    Gets the neighborhood data from the City of Chicago.
    Creates a dictionary with the khw or therms as keys and the neighborhoods
    as values.

    Input:
    l = list of data
    month = three letter lowercase value of month (e.g. "jan" or 
        can use "tot" for total in a year)
    """
    ranking_list = []
    d = coc_data.neighborhood_totals(l)

    for key in d.keys():
        #Normalize by population
        #print(l)
        if l == gas:
            total_pop_column = 14
        if l == l_elec:
            total_pop_column = 15    

        x = {float(d[key][month_dict[month]])/float(d[key][total_pop_column]):key}
        ranking_list.append(x)

    return ranking_list   

def sort(filename,month):
    """
    Given a csv file of interest and a month, this ranks the neighborhoods
    based on their electricity and gas consumption.
    """
    neighborhoods = determine_ranking(filename,month)
    l=[]
    for neighborhood in neighborhoods:
        for key in neighborhood.keys():
            l.append(round(key,10))

    sorted_values = quicksort.quick_sort(l,0,len(l)-1)
    rv = []
    for value in sorted_values:
        for neighborhood in neighborhoods:
            for key in neighborhood.keys():
                if value == round(key,10):
                    rv.append(neighborhood[key])
    #print(len(sorted_values))                
    #print(len(rv))
    return rv

def determine_census_ranking(l,month):

    ranking_list = {}

    with open ("census_energy_data.csv", "rt") as source:
        reader = csv.reader(source)
        header = next(reader, None)
        for row in reader:
            if float(row[14]) != 0:
                ranking_list[round(float(row[month_dict[month]+1])/float(row[14]),10)] = row[0]

    print(len(ranking_list))            
    return ranking_list        

def sort_census(filename,month):
    """
    Given a csv file of interest and a month, this ranks the neighborhoods
    based on their electricity and gas consumption.
    """

    blocks = determine_census_ranking(filename,month)

    l=[]
    for key in blocks.keys():
        l.append(round(key,10))

    sorted_values = quicksort.quick_sort(l,0,len(l)-1)

    rv = []

    for value in sorted_values:
        rv.append(blocks[value])

    return rv

if __name__=="__main__":
    ans = sort(l_elec,"tot")
    ans2 = sort(gas,"tot")

    print(ans)
    print(ans2)

    #ans3 = sort_census(l_elec,"tot")

    #print(ans3)
    #buildings = determine_building_ranking(l_elec,"tot")
    #ans3 = sort(l_elec)
    ans4 = sort_census(l_elec,"tot")
    print(len(ans4))
    ans5 = sort_census(gas,"tot")
    print(len(ans5))
