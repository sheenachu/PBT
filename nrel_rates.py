# Gets the utility rates for industrial, commerical, and residential
# buildings.
#
# Created by Kevin Bernat

import bs4
import utility
import pprint
import json

rates_url = "https://developer.nrel.gov/api/utility_rates/v3.xml?api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML"

def get_utility_rates(rates_url, address, lat, lon):
    """
    Given an address or latititude and longitude positions,
    return a dictionary with the electricity rate in $/(kWh)
    for residential, commercial, and industrial buildings.
    """

    d = {}

    if address != None:
        string = rates_url + "&address=" + address
    else:    
        string = rates_url + "&lat=" + lat + "&lon=" + lon

    print(string)

    request = utility.get_request(string)

    text =utility.read_request(request)
    soup = bs4.BeautifulSoup(text, "html5lib")
    
    commercial = soup.find("commercial")
    industrial = soup.find("industrial")
    residential = soup.find("residential")

    d["commercial"] = commercial.text
    d["industrial"] = industrial.text
    d["residential"] = residential.text

    return d


if __name__ == "__main__":

    get_utility_rates(rates_url, "6128 South Ellis Avenue", None, None) 