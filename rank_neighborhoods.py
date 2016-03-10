#Purpose: to add ranking information to neighborhood geojson properties

import json
import rankings
import coc_data

l_elec = coc_data.read_csv("Energy_Usage_2010_elec.csv")
l_gas = coc_data.read_csv("Energy_Usage_2010_therms.csv")

def read_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def rank():
    elec = rankings.sort(l_elec,"tot")
    gas = rankings.sort(l_gas,"tot")
    return elec, gas

def clean_ranks(data):
    for d in range(len(data)):
        if data[d] == 'Lakeview':
            data[d] = 'Lake View'
        if data[d] == "O'Hare":
            data[d] = 'OHare'

def update_json(n, rank, name):
    json_rejects = [] # not in json listing
    json_neighborhood_list = []
    rank_rejects = [] # not in rank listing

    rank_lower = []
    for r in rank:
        rank_lower.append(r.lower())

    for hood in n["features"]:
        prop = hood["properties"]
        if "pri_neigh" in prop:
            ID = "pri_neigh"
        else:
            ID = "community"
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

    print(json_rejects)
    print(rank_rejects)

def save_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

def process_json(input_f, output_f):
    neighborhoods = read_file(input_f)
    electricity, gas = rank()
    clean_ranks(electricity)
    clean_ranks(gas)
    update_json(neighborhoods, electricity, "elec_rank")
    update_json(neighborhoods, gas, "gas_rank")
    save_file(output_f, neighborhoods)





