import bs4
import utility
import pprint
import json

solar_url = "https://developer.nrel.gov/api/pvwatts/v4.xml?api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML&system_size="
#solar_url = "https://developer.nrel.gov/api/pvwatts/v4.xml?api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&system_size=4&dataset=tmy2&derate=0.77&lat=40&lon=-105&format=XML"
#solar_url = "https://developer.nrel.gov/api/pvwatts/v5.xml?api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&lat=40&lon=-105&system_capacity=4&azimuth=180&tilt=40&array_type=1&module_type=1&losses=10&format=XML"
#solar_url = "http://developer.nrel.gov/api/pvwatts/v5.json?api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&"

def visit_pv_pages(solar_url, address, system_size, lat, lon):
#def visit_pv_pages(solar_url, system_capacity, module_type, losses, array_type, tilt, azimuth, lat, lon):

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

    print(string)

    request = utility.get_request(string)

    text =utility.read_request(request)
    soup = bs4.BeautifulSoup(text, "html5lib")

    pp = pprint.PrettyPrinter()

    #prettyXML=soup.prettify() 
    #pp.pprint(prettyXML)

    ac_monthly = soup.find_all("ac-monthly")
    #dc_monthly = soup.find_all("dc-monthly")
    ac_annual = soup.find("ac-annual")
    #dc_annual = soup.find("dc-annual")

    d["ac_annual"] = ac_annual.text

    for index in range(1,len(soup.find_all('ac-monthly'))):
        d[index] = ac_monthly[index].text

    print(d)  
    return d  

if __name__ == "__main__":

    #x = visit_pv_pages(solar_url, None, "7", "41.7237152", "-88.1724365")    
    x = visit_pv_pages(solar_url, "6128 South Ellis Avenue", "7", None, None)    
