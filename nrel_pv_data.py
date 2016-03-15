# Determines the ac output of a hypothetical photovoltaic device.
#
# Created by Kevin Bernat



import bs4
import utility
import pprint
import json

solar_url = "https://developer.nrel.gov/api/pvwatts/v4.xml?api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML&system_size="

def visit_pv_pages(solar_url, address, system_size, lat, lon):

    """
    solar_url: url used to send request.
    system_size: PV capacity (kW). Number between 0.05 and 500000.
    address: address of building of interest (string)
    """

    d = {}

    if address != None:
        string = solar_url + system_size + "&address=" + address
    else:    
        string = solar_url + system_size + "&lat=" + lat + "&lon=" + lon

    request = utility.get_request(string)

    text =utility.read_request(request)
    soup = bs4.BeautifulSoup(text, "html5lib")

    pp = pprint.PrettyPrinter()

    ac_monthly = soup.find_all("ac-monthly")
    ac_annual = soup.find("ac-annual")

    d["ac_annual"] = ac_annual.text

    for index in range(1,len(soup.find_all('ac-monthly'))):
        d[index] = ac_monthly[index].text

    return d  

if __name__ == "__main__":

    x = visit_pv_pages(solar_url, "6128 South Ellis Avenue", "7", None, None)    
    print(x)