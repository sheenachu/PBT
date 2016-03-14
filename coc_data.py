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
            #l.append([','.join(row)])
    return l

def neighborhood(l):
    """
    Ignore this function...but might need for something else.
    """
    d = {}
    n = 0
    for row in l[1:]:
        neighborhood = row[0]
        print(neighborhood)
        if neighborhood not in d:

            d[neighborhood] = [{n:row[1:]}]
        else:
            d[neighborhood].append({n:row[1:]})    
        n += 1
            #if neighborhood not in d:
    print(d)
    return d        #    d[neighborhood] = neighborhood[1:]
    #print(d)   
def building_list(l):
    """
    Creates a list of the buildings in the City of Chicago data.
    They are ordered by as follows:
    {census_block:{building_type:{building_subtype:list of other information}}}
    """

    #building_list = []
    building_dict ={}

    for row in l[1:]:
        if row[1] != '' and row[2] != '' and row[3] != '':
            census_block = row[1]
            #print(census_block)
            building_type = row[2]
            building_subtype = row[3]
            #try:
            #    duplicate = building_dict[census_block][building_type][building_subtype]
            #    print(row)
            #except KeyError:
            #    pass
            if census_block not in building_dict:
                building_dict[census_block] = [{building_type:{building_subtype:[row[0]] + row[4:]}}]
            else:
                building_dict[census_block].append({building_type:{building_subtype:[row[0]] + row[4:]}})

    #print(building_dict)
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
    Given an address, building type, and building subtype,
    the appropriate row from the City of Chicago data is selected.
    """

    coords = coords_to_block.addr_to_coords(coords_to_block.address_url, address)   
    census_block = coords_to_block.visit_pages(coords_to_block.url,coords)
    #if building_subtype == None:

    #    ans = building_dict[str(census_block)][building_type] 

    matches = building_dict[str(census_block)]

    for match in matches:
        print(match)

        #try:
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
        #except KeyError:
        #    ans = "Not Found"
   # try:

   #     ans = building_dict[str(census_block)][0][building_type][building_subtype]
   # except KeyError:
    # == 'Multi 7+' or KeyError == 'Multi <7' or KeyError == 'Single Family':
   #     ans = building_dict[str(census_block)][0][building_type] 

    return ans

def census_block_data(l, filename):

    d = {}
    for row in l[1:]:
        if '' in row:
            pass
        else:    
            #print(row[4:16])
            #for i in row[4:17]:
            #    if i == '':
            #        pass
            #    else:    
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

                            #for value in values:
                                #print(type(value))
                            #print(row[1],[row[4:17]])
                    d[row[1]] = values

                else:
                    if filename == "Energy_Usage_2010_elec.csv":
                        values = np.array(row[4:17] + [0])
                    if filename == "Energy_Usage_2010_therms.csv":
                        values = np.array(row[4:17] + [0])

                    values = values + d[row[1]]
                    #print(row[1],values)
                    d[row[1]] = values 
                        #print(d[row[1]])  
    return d  
def census_csv(census_block_dict,filename):
     with open(filename, "wt") as result:
        writer = csv.writer(result)
        writer.writerow(("census","jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec","tot","population"))
        for key in census_block_dict.keys():
            writer.writerow((key, census_block_dict[key][0], census_block_dict[key][1],
                census_block_dict[key][2],census_block_dict[key][3],census_block_dict[key][4],
                census_block_dict[key][5],census_block_dict[key][6],census_block_dict[key][7],
                census_block_dict[key][8],census_block_dict[key][9],census_block_dict[key][10],
                census_block_dict[key][11],census_block_dict[key][12],census_block_dict[key][13]))



#key = [COMMUNITY AREA NAME,CENSUS BLOCK,BUILDING TYPE,BUILDING_SUBTYPE,
#KWH JANUARY 2010,KWH FEBRUARY 2010,KWH MARCH 2010,KWH APRIL 2010,
#KWH MAY 2010,KWH JUNE 2010,KWH JULY 2010,KWH AUGUST 2010,
#KWH SEPTEMBER 2010,KWH OCTOBER 2010,KWH NOVEMBER 2010,
#KWH DECEMBER 2010,TOTAL KWH,ELECTRICITY ACCOUNTS,ZERO KWH ACCOUNTS,
#THERM JANUARY 2010,THERM FEBRUARY 2010,THERM MARCH 2010,
#TERM APRIL 2010,THERM MAY 2010,THERM JUNE 2010,THERM JULY 2010,
#THERM AUGUST 2010,THERM SEPTEMBER 2010,THERM OCTOBER 2010,
#THERM NOVEMBER 2010,THERM DECEMBER 2010,TOTAL THERMS,GAS ACCOUNTS,
#KWH TOTAL SQFT,THERMS TOTAL SQFT,KWH MEAN 2010,
#KWH STANDARD DEVIATION 2010,KWH MINIMUM 2010,KWH 1ST QUARTILE 2010,
#KWH 2ND QUARTILE 2010,KWH 3RD QUARTILE 2010,KWH MAXIMUM 2010,
#KWH SQFT MEAN 2010,KWH SQFT STANDARD DEVIATION 2010,
#KWH SQFT MINIMUM 2010,KWH SQFT 1ST QUARTILE 2010,
#KWH SQFT 2ND QUARTILE 2010,KWH SQFT 3RD QUARTILE 2010,
#KWH SQFT MAXIMUM 2010,THERM MEAN 2010,THERM STANDARD DEVIATION 2010,
#THERM MINIMUM 2010,THERM 1ST QUARTILE 2010,THERM 2ND QUARTILE 2010,
#THERM 3RD QUARTILE 2010,THERM MAXIMUM 2010,THERMS SQFT MEAN 2010,
#THERMS SQFT STANDARD DEVIATION 2010,THERMS SQFT MINIMUM 2010,
#THERMS SQFT 1ST QUARTILE 2010,THERMS SQFT 2ND QUARTILE 2010,
#THERMS SQFT 3RD QUARTILE 2010,THERMS SQFT MAXIMUM 2010,TOTAL POPULATION,
#TOTAL UNITS,AVERAGE STORIES,AVERAGE BUILDING AGE,AVERAGE HOUSESIZE,
#OCCUPIED UNITS,OCCUPIED UNITS PERCENTAGE,RENTER-OCCUPIED HOUSING UNITS,
#RENTER-OCCUPIED HOUSING PERCENTAGE,OCCUPIED HOUSING UNITS]
