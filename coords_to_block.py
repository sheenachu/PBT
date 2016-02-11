import bs4
import utility
import pprint
import json
import re

url = "http://data.fcc.gov/api/block/2010/find?"

def visit_pages(url, lat, lon):

    url = url + "latitude=" + lat + "&longitude=" + lon
    request = utility.get_request(url)

    text =utility.read_request(request)
    soup = bs4.BeautifulSoup(text, "html5lib")

    census_block = soup.find('block')
    stripped_census_block = re.sub('[^0-9]', ' ', str(census_block))
    code_list = stripped_census_block.split()
    census_block = code_list[0]

    return census_block

    #pp = pprint.PrettyPrinter()

    #prettyXML=soup.prettify() 
    #pp.pprint(prettyXML)