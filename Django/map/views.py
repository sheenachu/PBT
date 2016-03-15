#------------------------------------
# Includes code: 
#   modified from CS122: PA3
#   written by Kevin Bernat
#   written by Estelle Ostro
#------------------------------------

from django.shortcuts import render
from django import forms
import coords_to_block as cbt


def map(request):
    context = {}
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = AddressForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            # Convert form data to an args dictionary for find_courses
            block = form.cleaned_data
            rv = calculate_census_block(block['address'])  
            rv = rv[5:9]
            if rv == None:
                rv = 'Please submit a valid address.'
            context['block'] = rv
    else:
        form = SearchForm(initial={'address' : '123 Main St Chicago, IL'})
  
    context['form'] = form
    return render(request, 'map/map.html', context)

class AddressForm(forms.Form):
    address = forms.CharField(label='Your Address', max_length=200)


def addr_to_coords(address_url, address):
    """
    Converts an address to the latitude and longitude locations.
    """

    complete_url = address_url + address
    request = utility.get_request(complete_url)

    text = utility.read_request(request)
    soup = bs4.BeautifulSoup(text, "html5lib")

    lat = soup.find("lat")
    lon = soup.find("lng")

    if lat == None or lon == None:
        return None
    return[lat.text,lon.text]

def visit_pages(url,coords):    
    """
    Given a url and coordinates, this returns the corresponding census
    block the coordinates fall under. This will then be used to compare
    the census block data to the photovoltaic data
    """
    if coords == None:
        return None

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

    coords = cbt.addr_to_coords(address_url, address)   
    rv = cbt.visit_pages(url,coords)
    return rv