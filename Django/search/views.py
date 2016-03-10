#------------------------------------
# Code modified from CS122: PA3
#------------------------------------

from django.shortcuts import render
from django.http import HttpResponse
from django import forms
import json
import traceback
from io import StringIO
import sys
import csv
import os
from operator import and_
from courses import find_courses
from functools import reduce

NOPREF_STR = 'No preference'
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')
COLUMN_NAMES = dict(
        dev='Device',
        day='Day',
)


def _valid_result(res):
    """Validates results returned by find_courses"""
    (HEADER, RESULTS) = [0,1]
    ok = (isinstance(res, (tuple, list)) and 
          len(res) == 2 and
          isinstance(res[HEADER], (tuple, list)) and
          isinstance(res[RESULTS], (tuple, list)))
    if not ok:
        return False

    n = len(res[HEADER])
    def _valid_row(row):
        return isinstance(row, (tuple, list)) and len(row) == n
    return reduce(and_, (_valid_row(x) for x in res[RESULTS]), True)

def _load_column(filename, col=0):
    """Loads single column from csv file"""
    with open(filename) as f:
        col = list(zip(*csv.reader(f)))[0]
        return list(col)


def _load_res_column(filename, col=0):
    """Load column from resource directory"""
    return _load_column(os.path.join(RES_DIR, filename), col=col)


def _build_dropdown(options):
    """Converts a list to (value, caption) tuples"""
    return [(x, x) if x is not None else ('', NOPREF_STR) for x in options]

DAYS = _build_dropdown(_load_res_column('day_list.csv'))
DEVICE = _build_dropdown([None] + _load_res_column('device.csv'))

class SearchForm(forms.Form):

    dev = forms.ChoiceField(label='Device', choices=DEVICE, required=False)
    days = forms.MultipleChoiceField(label='Days',
                                     choices=DAYS,
                                     widget=forms.CheckboxSelectMultiple,
                                     required=False)

def improve(request):
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():

            # Convert form data to an args dictionary for find_courses
            args = {}
            # if form.cleaned_data['query']:
            #     args['terms'] = form.cleaned_data['query']
            days = form.cleaned_data['days']
            if days:
                args['day'] = days
            dev = form.cleaned_data['device']
            if dev:
                args['dev'] = dev

            # if form.cleaned_data['show_args']:
            #     context['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)

            try:
                res = find_courses(args)
            except Exception as e:
                print('Exception caught')
                bt = traceback.format_exception(*sys.exc_info()[:3])
                context['err'] = """
                An exception was thrown in find_courses:
                <pre>{}
{}</pre>
                """.format(e, '\n'.join(bt))

                res = None
    else:
        form = SearchForm()

    # Handle different responses of res
    if res is None:
        context['result'] = None
    elif isinstance(res, str):
        context['result'] = None
        context['err'] = res
        result = None
        cols = None
    elif not _valid_result(res):
        context['result'] = None
        context['err'] = ('Return of find_courses has the wrong data type. '
                         'Should be a tuple of length 4 with one string and three lists.')
    else:
        columns, result = res

        # Wrap in tuple if result is not already
        if result and isinstance(result[0], str):
            result = [(r,) for r in result]

        context['result'] = result
        context['num_results'] = len(result)
        context['columns'] = [COLUMN_NAMES.get(col, col) for col in columns]

    context['form'] = form
    return render(request, 'search/search.html', context)

def home(request):
    return render(request, 'search/index.html', {})