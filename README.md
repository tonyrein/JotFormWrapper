JotFormWrapper

A non-profit agency where I volunteer planned to use a JotForm [(](https://www.jotform.com/)[www.jotform.com](http://www.jotform.com/)[)](https://www.jotform.com/) to register participants in an event, and found that it did not quite meet all their requirements. I wrote JotFormWrapper in an attempt to add the functionality they needed.

The library teamnameswrapper.py is the heart of JotFormWrapper. It packages up calls to JotForm’s api (<https://api.jotform.com/docs/>) in order to provide the methods used by the routes in the Bottle app contained in add\_name\_api.py.
