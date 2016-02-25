import bs4
import utility
import pprint
import json

#Get alternative fuel stations data


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

solar_url = "https://developer.nrel.gov/api/pvwatts/v4.xml?system_size=7&"

url_list =[url,url2, url3,url4,url5,url6,url7,url8,url9,url10,url11, url12]

def visit_alt_fuel_pages(url_list):
    d = {}
    n = 0
    for url in url_list:

        request = utility.get_request(url)

        text =utility.read_request(request)
        soup = bs4.BeautifulSoup(text, "html5lib")

        #pp = pprint.PrettyPrinter()

        #prettyXML=soup.prettify() 
        #pp.pprint(prettyXML)

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

if __name__ == "__main__":
    visit_alt_fuel_pages(url_list) 