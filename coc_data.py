import csv
#l = []

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
    return d        #    d[neighborhood] = neighborhood[1:]
    #print(d)   

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
