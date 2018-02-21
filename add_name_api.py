#!/usr/bin/env python2
"""
Bottle REST API to allow Web page
to add a team name without knowing
any secret API keys.


EXAMPLES:

To get a list of team names:

 curl http://localhost:9000/names


To add a new name:

 curl http-X POST -H "Content-Type:application/json" -d '{ "teamname":"Walk Tall"}' http://server:port/names
 
The new name will be put into Proper Case (first letter of each word capitalized, rest lower-case). In addition,
all characters except for A-Z, a-z, 0-9, '-', and whitespace will be replaced with underscores ('_') and all
multiple-whitespace sequences will be replaced with single spaces.

If the new name is a duplicate of an already-existing name, Error 409 will be returned to the web client; otherwise,
status 200 will be returned, along with the json-encoded name that was added. For example:
  {"teamname": "Fast Hombres"}

"""
import bottle
from bottle import request, response, post, get, default_app
from teamnameswrapper import TeamFormsWrapper
from allow_cors import *

import json
from urllib2 import HTTPError

RO_KEY='<YOUR JOTFORM READ-ONLY API KEY HERE>'
RW_KEY='<YOUR JOTFORM READ-WRITE API KEY HERE>'

# API client to interact with Jotform form:
api = TeamFormsWrapper(RO_KEY, RW_KEY)

@get('/teamnames')
def get_team_names():
    """
    Return a list of names, json-encoded
    """
    try:
        current_names = api.current_names
        if current_names is None:
            raise ValueError
        response.headers['Content-Type']='application/json'
        response.headers['Cache-Control']='no-cache'
        return json.dumps(current_names)
    except:
        # return error response:
        response.status = 400
        return
    
@post('/teamnames')
def add_team_name():
    """ 
    Handles addition of a new team name.
    Validation is done by the RegFormWrapper.
    Return "prettified" and "sanitized" name added.
    """
    try:
        data = request.json
        if data is None:
            raise ValueError('No data supplied')
        name_added = api.add_team_name(data['teamname'])
        # Return success!
        response.status = 200
        response.headers['Content-Type'] = 'application/json'
        return json.dumps( {'teamname': name_added } )
    except ValueError, e:
        # return error response:
        response.status = 400
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({'error': e.message })
    except KeyError, e:
        response.status = 409
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({'error': e.message })


@get('/teamnames/<onename>')
def get_single_name(onename):
    """
    Since the name passed here isn't the key to anything, but is
    the thing itself, there aren't many use cases for a GET call with
    a single name. One such use case is to check if a name is already
    in use.
    
    If the name exists, return status 200 and { 'teamname': MASSAGED_NAME, 'available': 'no' },
    where MASSAGED_NAME is the sanitized and prettified version of the
    name originally supplied.
    
    If the name does not exist, return status 200 and { 'teamname': MASSAGED_NAME, 'available': 'yes' }
    """
    try:
        if not onename:
            raise ValueError('No data supplied')
        # name_already_there will be "" if no such name is already in use.
        nameDict = api.is_name_available(onename)
        print(nameDict)
        # Return success!
        response.status = 200
        response.headers['Content-Type'] = 'application/json'
        return json.dumps( nameDict )
    except ValueError, e:
        # return error response:
        response.status = 400
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({'error': e.message })

@post('/teamform/')
def submit_add_team_form():
    try:
        data = request.json
        if data is None:
            raise ValueError
        result = api.submit_add_team_form(data)
        # Return success!
        response.status = 200
        response.headers['Content-Type'] = 'application/json'
        return json.dumps( {'submission_id': result } )
    except HTTPError, e:
        # return error response:
        response.status = e.code
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({'error': e.message })
    
app = application = default_app()
if __name__ == '__main__':
    bottle.run( host='localhost', port='8080')
