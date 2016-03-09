#Purpose: Determine the ranking of the different neighborhoods
# in Chicago
#
# Created by Kevin Bernat
#

import coc_data
import quicksort

l_elec = coc_data.read_csv("Energy_Usage_2010_elec.csv")
gas = coc_data.read_csv("Energy_Usage_2010_therms.csv")

def determine_ranking(l):
    ranking_list = []
    d = coc_data.neighborhood_totals(l)

    for key in d.keys():
        #Normalize by population
        x = {float(d[key][17])/float(d[key][-10]):key}
        ranking_list.append(x)
    #print(ranking_list)
    return ranking_list   

def sort(filename):
    neighborhoods = determine_ranking(filename)
    l=[]
    for neighborhood in neighborhoods:
        for key in neighborhood.keys():
            l.append(round(key,10))
    #print(l)
    sorted_values = quicksort.quick_sort(l,0,len(l)-1)
    rv = []
    for value in sorted_values:
    #    print("value ",value)
        for neighborhood in neighborhoods:
            for key in neighborhood.keys():
    #            print("key ", key)
                if value == round(key,10):
    #                print('got here')
                    rv.append(neighborhood[key])
    #print(len(sorted_values))                
    #print(len(rv))
    return rv

if __name__=="__main__":
    ans = sort(l_elec)
    ans2 = sort(gas)

    print(ans)
    print(ans2)
