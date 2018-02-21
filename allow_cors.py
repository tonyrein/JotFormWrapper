"""
Import this to configure the bottle app
to signal to clients that Cross-Origin Resource Sharing
is OK.

From https://www.toptal.com/bottle/building-a-rest-api-with-bottle-framework

For explanations, see above-referenced page, and also
http://www.primaryobjects.com/2011/08/29/cross-domain-policy-violation-and-how-to-get-around-it-jsonp-ajax-javascript/
and
https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy

"""
from bottle import hook, route, response

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

@hook('after_request')
def enable_cors():
    '''Add headers to enable CORS'''
    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers

@route('/', method = 'OPTIONS')
@route('/<path:path>', method = 'OPTIONS')
def options_handler(path = None):
    return
