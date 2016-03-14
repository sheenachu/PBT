import bs4
import utility
import pprint
import json
from math import radians, cos, sin, asin, sqrt
import coords_to_block

address_url = "https://maps.googleapis.com/maps/api/geocode/xml?&key=AIzaSyAOnOrIMatS8PArWxa-o2qkZ6Nutzi_a98&address="

#There is a limit to the number of zip codes that can be 
#inputted at a time. These urls encompass all the zip codes
#in Chicago.


url = "https://developer.nrel.gov/api/alt-fuel-stations/v1.xml?fuel_type=all&state=IL&zip=60601,60602,60603,60604,60605&limit=100&api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML"
url2 = "https://developer.nrel.gov/api/alt-fuel-stations/v1.xml?fuel_type=all&state=IL&zip=60607,60608,60609,60610&limit=100&api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML"
url3 = "https://developer.nrel.gov/api/alt-fuel-stations/v1.xml?fuel_type=all&state=IL&zip=60611,60612,60613,60614,60615&limit=100&api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML"
url4 = "https://developer.nrel.gov/api/alt-fuel-stations/v1.xml?fuel_type=all&state=IL&zip=60616,60617,60618,60619,60620&limit=100&api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML"
url5 = "https://developer.nrel.gov/api/alt-fuel-stations/v1.xml?fuel_type=all&state=IL&zip=60621,60622,60623,60624,60625&limit=100&api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML"
url6 = "https://developer.nrel.gov/api/alt-fuel-stations/v1.xml?fuel_type=all&state=IL&zip=60626,60628,60629,60630,60631&limit=100&api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML"
url7 = "https://developer.nrel.gov/api/alt-fuel-stations/v1.xml?fuel_type=all&state=IL&zip=60632,60633,60634,60635,60636&limit=100&api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML"
url8 = "https://developer.nrel.gov/api/alt-fuel-stations/v1.xml?fuel_type=all&state=IL&zip=60637,60638,60639,60640,60641&limit=100&api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML"
url9 = "https://developer.nrel.gov/api/alt-fuel-stations/v1.xml?fuel_type=all&state=IL&zip=60643,60644,60645,60646,60647&limit=100&api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML"
url10 = "https://developer.nrel.gov/api/alt-fuel-stations/v1.xml?fuel_type=all&state=IL&zip=60649,60651,60652,60653,60655&limit=100&api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML"
url11 = "https://developer.nrel.gov/api/alt-fuel-stations/v1.xml?fuel_type=all&state=IL&zip=60656,60657,60659,60660,60661&limit=100&api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML"
url12 = "https://developer.nrel.gov/api/alt-fuel-stations/v1.xml?fuel_type=all&state=IL&zip=60666,60827&limit=100&api_key=78WBQrMES4pXDbTB1W4To32M3R6fRLOO5W6x35n5&format=XML"

#solar_url = "https://developer.nrel.gov/api/pvwatts/v4.xml?system_size=7&"

url_list =[url,url2, url3,url4,url5,url6,url7,url8,url9,url10,url11, url12]

def visit_alt_fuel_pages(url_list):
    """
    Given a list of urls with different zip codes in Chicago, it
    returns a dictionary with data on alternative fuel stations
    in the following format: {n:[station name, address, city,
    latitude,longitude,alternative fuel type, status (E for Open,
        P for planned, T for temporarily unavailable)]}

    alternative fuel type options:

    BD      Biodiesel (B20 and above)
    CNG     Compressed Natural Gas
    E85     Ethanol (E85)
    ELEC    Electric
    HY      Hydrogen
    LNG     Liquefied Natural Gas
    LPG     Liquefied Petroleum Gas (Propane)


    """
    d = {}
    n = 0
    for url in url_list:

        request = utility.get_request(url)

        text =utility.read_request(request)
        soup = bs4.BeautifulSoup(text, "html5lib")

        city = soup.find_all('city')
        ft = soup.find_all('fuel-type-code')
        lat = soup.find_all('latitude')
        lon = soup.find_all('longitude')
        sn = soup.find_all('station-name')
        sa = soup.find_all('street-address')
        sc = soup.find_all('status-code')

        for index in range(len(soup.find_all('fuel-station'))):
            string = str(sn[index].text) + "|" + str(sa[index].text) + "|"+ str(city[index].text) + "|"+ str(lat[index].text) + "|"+ str(lon[index].text) + "|"+ str(ft[index].text) + "|"+ str(sc[index].text)
            station_list = string.split("|")
            d[n] = station_list 

            n+= 1 

    print(d)           
    return d          

#The distance function was retrieved from: http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
def distance(lat1,lon1,lat2,lon2):
    """
    Calculates the distance between two latitude and longitude
    positions.
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def find_nearest(address, address_url, url_list):
    """
    Finds the nearest alternative fuel station based on a
    given address. Returns a list with information on 
    the  alternative fuel station and the distance in km
    between the station and the address.
    """
    shortest_distance = 10000
    fuel_station = ''
    fuel_list = visit_alt_fuel_pages(url_list)
    print('got here')
    coords = coords_to_block.addr_to_coords(address_url, address)
    for station in fuel_list:
        #print(fuel_list[station][3])
        check_distance = distance(float(coords[0]),float(coords[1]),float(fuel_list[station][3]),float(fuel_list[station][4]))
        print(check_distance)
        if shortest_distance > check_distance:
            shortest_distance = check_distance
            fuel_station = fuel_list[station]

    return fuel_station + [shortest_distance]        


if __name__ == "__main__":
    ans = find_nearest("6128 South Ellis Avenue, Chicago, IL",address_url,url_list)
    print(ans)
    #visit_alt_fuel_pages(url_list) 