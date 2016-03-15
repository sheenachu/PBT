#------------------------------------
# Includes code: 
#   modified from CS122: PA3
#   written by Kevin Bernat, Estelle Ostro, and Sheena Chu
#------------------------------------

from django.shortcuts import render
from django import forms
import coords_to_block as cbt

def census(request):

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
        form = SearchForm(initial={'address' : '123 Main St Chicago, IL'})
  
    context['form'] = form

    return render(request, 'map/census.html', context)

class AddressForm(forms.Form):
    address = forms.CharField(label='Your Address', max_length=200, required=False)

def calculate_census_block(address):
    url = "http://data.fcc.gov/api/block/2010/find?"
    address_url = "https://maps.googleapis.com/maps/api/geocode/xml?&key=AIzaSyAOnOrIMatS8PArWxa-o2qkZ6Nutzi_a98&address="

    coords = cbt.addr_to_coords(address_url, address)   
    rv = cbt.visit_pages(url,coords)
    return coords, rv

def map(request):
    return render(request, 'map/map.html', {})
