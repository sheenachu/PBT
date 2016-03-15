import bs4
import utility
import pprint
import json
import re

url = "http://data.fcc.gov/api/block/2010/find?"
address_url = "https://maps.googleapis.com/maps/api/geocode/xml?&key=AIzaSyAOnOrIMatS8PArWxa-o2qkZ6Nutzi_a98&address="

def addr_to_coords(address_url, address):
    """
    Converts an address to the latitude and longitude locations.
    """

    complete_url = address_url + address
    request = utility.get_request(complete_url)

    text =utility.read_request(request)
    soup = bs4.BeautifulSoup(text, "html5lib")

    lat = soup.find("lat")
    lon = soup.find("lng")
    return[lat.text,lon.text]

#def visit_pages(url, lat, lon):
def visit_pages(url,coords):    
    """
    Given a url and coordinates, this returns the corresponding census
    block the coordinates fall under. This will then be used to compare
    the census block data to the photovoltaic data
    """

    url = url + "latitude=" + coords[0] + "&longitude=" + coords[1]
    request = utility.get_request(url)

    text =utility.read_request(request)
    soup = bs4.BeautifulSoup(text, "html5lib")

    census_block = soup.find('block')
    stripped_census_block = re.sub('[^0-9]', ' ', str(census_block))
    code_list = stripped_census_block.split()
    census_block = code_list[0]
    return census_block

def calculate_census_block(address):
    url = "http://data.fcc.gov/api/block/2010/find?"
    address_url = "https://maps.googleapis.com/maps/api/geocode/xml?&key=AIzaSyAOnOrIMatS8PArWxa-o2qkZ6Nutzi_a98&address="

    coords = addr_to_coords(address_url, address)   
    visit_pages(url,coords)

