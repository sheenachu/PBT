import bs4
import utility
import pprint
import json

solar_url = "https://developer.nrel.gov/api/pvwatts/v4.xml?api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML&system_size="
#solar_url = "https://developer.nrel.gov/api/pvwatts/v4.xml?api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&system_size=4&dataset=tmy2&derate=0.77&lat=40&lon=-105&format=XML"
#solar_url = "https://developer.nrel.gov/api/pvwatts/v5.xml?api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&lat=40&lon=-105&system_capacity=4&azimuth=180&tilt=40&array_type=1&module_type=1&losses=10&format=XML"

def visit_pv_pages(solar_url, system_size, lat, lon):
    """
    solar_url: url used to send request.
    system_size: PV capacity (kW). Number between 0.05 and 500000.
    address: address of building of interest (string)
    """
    #string = solar_url + system_size + "&address=" + address + "&lat=" + lat + "&lon" + lon
    string = solar_url + system_size + "&lat=" + lat + "&lon" + lon

    print(string)

    request = utility.get_request(string)

    text =utility.read_request(request)
    soup = bs4.BeautifulSoup(text, "html5lib")

    pp = pprint.PrettyPrinter()

    prettyXML=soup.prettify() 
    pp.pprint(prettyXML)

def test(solar_url):  

    request = utility.get_request(solar_url)

    text =utility.read_request(solar_url)
    soup = bs4.BeautifulSoup(text, "html5lib")

    pp = pprint.PrettyPrinter()

    prettyXML=soup.prettify() 
    pp.pprint(prettyXML)

    print(soup)

if __name__ == "__main__":

    visit_pv_pages(solar_url, "7", "41.7237152", "-88.1724365")    
    #visit_pv_pages(solar_url, "7","41.", "-88.")    
    #test(solar_url)
