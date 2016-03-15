#------------------------------------
# Purpose:
#   Creates a Django form which retrieves the census tract of a submitted 
#   address.
#
# Includes code: 
#   modified from CS122: PA3
#   modified from https://docs.djangoproject.com/en/1.9/topics/forms/
#   written by Estelle Ostro
#------------------------------------

from django.shortcuts import render
from django import forms
import coords_to_block as cbt

URL = "http://data.fcc.gov/api/block/2010/find?"
ADDRESS_URL = "https://maps.googleapis.com/maps/api/geocode/xml?&key=AIzaSyAOnOrIMatS8PArWxa-o2qkZ6Nutzi_a98&address="


def census(request):
    '''
    Creates a form which retrieves the census tract of a submitted address and
    generates the census map webpage
    '''
    context = {}
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = AddressForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            # Convert form data to an args dictionary for find_courses
            block = form.cleaned_data
            coords, rv = calculate_census_block(block['address'])  
            if rv == None:
                rv = 'Please submit a valid address.'
            else:
                rv = rv[5:9]
            context['block'] = rv
            context['coords'] = coords
    else:
        form = SearchForm()
  
    context['form'] = form

    return render(request, 'map/census.html', context)

class AddressForm(forms.Form):
    '''
    Creates a form for submitting an address
    '''
    address = forms.CharField(label='Your Address', max_length=200, required=False)

def calculate_census_block(address):
    '''
    Calculates the census block of a given address
    '''
    coords = cbt.addr_to_coords(ADDRESS_URL, address)   
    rv = cbt.visit_pages(URL,coords)
    return coords, rv

def map(request):
    '''
    Generates the neighborhood map webpage
    '''
    return render(request, 'map/map.html', {})
