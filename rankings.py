# Purpose: Determine the ranking of the different neighborhoods
# in Chicago
#
# Created by Kevin Bernat
#

import coc_data
import quicksort

l_elec = coc_data.read_csv("Energy_Usage_2010_elec.csv")
gas = coc_data.read_csv("Energy_Usage_2010_therms.csv")
month_dict = {"jan":1, "feb":2, "mar":3, "apr":4, "may":5,
"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12,"tot":13}

def determine_ranking(l,month):
    """
    Gets the neighborhood data from the City of Chicago.
    Creates a dictionary with the khw or therms as keys and the neighborhoods
    as values.
    """
    ranking_list = []
    d = coc_data.neighborhood_totals(l)

    for key in d.keys():
        #Normalize by population

        x = {float(d[key][month_dict[month]+4])/float(d[key][-10]):key}
        ranking_list.append(x)
    #print(ranking_list)
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

if __name__=="__main__":
    ans = sort(l_elec,"tot")
    ans2 = sort(gas,"tot")

    print(ans)
    print(ans2)
