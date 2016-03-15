#------------------------------------
# Purpose: 
#   To add ranking information to neighborhood/census geojson 
#   properties
# Includes code: 
#   written by Estelle Ostro
#------------------------------------


import json
import rankings
import coc_data

l_elec = coc_data.read_csv("Energy_Usage_2010_elec.csv")
l_gas = coc_data.read_csv("Energy_Usage_2010_therms.csv")

def read_file(filename):
    '''
    Read a geojson file
        filename: input filename (str)
    '''
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def rank():
    '''
    Calculate electricity & gas rankings by neighborhood
    '''
    elec = rankings.sort(l_elec,"tot")
    gas = rankings.sort(l_gas,"tot")
    return elec, gas

def census_rank():
    '''
    Calculate electricity and gas rankings by census tract
    '''
    elec = rankings.sort_census("census_energy_data_elec.csv","tot")
    gas = rankings.sort_census("census_energy_data_therms.csv","tot")
    return elec, gas

def clean_ranks(data):
    '''
    Clean neighborhood rank list to work with geojson data format
        data: geojson neighborhood data
    '''
    for d in range(len(data)):
        if data[d] == 'Lakeview':
            data[d] = 'Lake View'
        if data[d] == "O'Hare":
            data[d] = 'OHare'

def update_json(n, rank, name, input_type):
    '''
    Update the geojson dict with given ranking property
        n: geojson data to be modified
        rank: ranked neighborhoods/tracts
        name: geojson property name (str)
        input_type: 'neighborhood' or 'census'
    '''
    #For troubleshooting:
    json_rejects = [] # not in json listing
    json_neighborhood_list = []
    rank_rejects = [] # not in rank listing

    rank_lower = []
    if input_type == 'neighborhood':
        for r in rank:
            rank_lower.append(r.lower())
    else:
        for r in rank:
            rank_lower.append(r[5:11])

    for hood in n["features"]:
        prop = hood["properties"]
        if input_type == 'neighborhood':
            if "pri_neigh" in prop:
                ID = "pri_neigh"
            else:
                ID = "community"
        if input_type == 'census':
            ID = "tractce10"
        json_neighborhood_list.append(prop[ID].lower())
        if prop[ID].lower() in rank_lower:
            r = rank_lower.index(prop[ID].lower()) + 1
            prop.update({name : r})
        else:
            prop.update({name : 0})
            rank_rejects.append(prop[ID])
    for r in rank_lower:
        if r not in json_neighborhood_list:
            json_rejects.append(r)



def save_file(filename, data):
    '''
    Save the modified geojson data to a new file
        filename: output filename (str)
        data: geojson data
    '''
    with open(filename, 'w') as f:
        json.dump(data, f)

def process_json(input_f, output_f, input_type):
    '''
    Update a geojson file with ranking info
        input_f: input filename (str)
        output_f: output filename (str)
        input_type: 'neighborhood' or 'census 
    '''
    if input_type == 'neighborhood':
        neighborhoods = read_file(input_f)
        electricity, gas = rank()
        clean_ranks(electricity)
        clean_ranks(gas)
        update_json(neighborhoods, electricity, "elec_rank", input_type)
        update_json(neighborhoods, gas, "gas_rank", input_type)
        save_file(output_f, neighborhoods)
    elif input_type == 'census':
        tracts = read_file(input_f)
        electricity, gas = census_rank()
        update_json(tracts, electricity, "elec_rank", input_type)
        update_json(tracts, gas, "gas_rank", input_type)
        save_file(output_f, tracts)






