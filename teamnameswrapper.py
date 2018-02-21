"""
    A class that wraps a couple of Jotform API functions.
    
    Tony Rein (crjcvg@gmail.com)
    2017-02-02
    
    The JotForm Python API has not been ported to Python 3; therefore,
    this class needs Python 2.

    For documentation of the JotForm api. see here:
        http://api.jotform.com/docs/

"""

import re

import jotform

# You need to find the following values by looking
# at the page source of the JotForm you're trying
# to interact with.
TEAM_NAME_QUESTION = 'XX'
REG_FORM_ID = 'YYYYYYYYYYYYYYYY'
ADD_TEAM_FORM_ID = 'ZZZZZZZZZZZZZZZZZZ'

class TeamFormsWrapper(object):
    def __init__(self, readOnlyAPIKey, readWriteAPIKey = None):
        self._readOnlyClient = jotform.JotformAPIClient(readOnlyAPIKey)
        if readWriteAPIKey is not None:
            self._readWriteClient = jotform.JotformAPIClient(readWriteAPIKey)
        else:
            self._readWriteClient = None
        # List of characters allowed in team names:
        # (upper- and lower-case ASCII, digits 0-9, whitespace, dash, and underscore).
        self._namepattern = re.compile('[^\w\s-]+')
        self.current_names = []
        self._load_team_names()

    @property
    def readOnlyClient(self):
        return self._readOnlyClient
    @property
    def readWriteClient(self):
        return self._readWriteClient
    @property
    def current_names(self):
        return self._current_names
    @current_names.setter
    def current_names(self, newlist):
        self._current_names = newlist if newlist else []
    
    def _prettify_name(self, old_name):
        """
        Put into Title Case and coalesce all multi-whitespace
        sequences into a single space character.
        """
        s = old_name.title()
        return " ".join(s.split())


    def _sanitize_name(self, old_name):
        """
        Replace any character that's not in allowed list
        with "_". The list of allowed characters is set by the
        definition of the variable 'namepattern' above.
        """
        return self._namepattern.sub('_',old_name)
        
    """
    Set self.current_names to list of UTF-8 strings
    """        
    def _load_team_names(self):
        try:
            question = self.readOnlyClient.get_form_question(REG_FORM_ID, TEAM_NAME_QUESTION)
            self.current_names = question['options'].split('|')
            self.current_names.sort()
        except Exception, e:
            raise ValueError('Could not get question info from Jotform: {}'.format(e.message))
    
    """
        Set Jotform's list of team names from self.current_names
    """        
    def _save_team_names(self):
        if self.current_names is None:
            raise ValueError('No current names list')
        try:
            question = self.readWriteClient.get_form_question(REG_FORM_ID, TEAM_NAME_QUESTION)
            question['options'] = '|'.join(self.current_names)
            self.readWriteClient.edit_form_question(REG_FORM_ID, TEAM_NAME_QUESTION, question)
        except:
            raise ValueError("Could not set Jotform's list of team names: {}".format(e.message))
    
    """
        Pass: name to add (UTF-8 string)
        If name added OK, return sanitized and
        prettified version of the name; otherwise,
        raise KeyError
    """
    def add_team_name(self, new_name):
        if new_name is None:
            raise ValueError('No name supplied')
        name_to_check = new_name.strip()
        name_to_check = self._sanitize_name(name_to_check)
        name_to_check = self._prettify(name_to_check)
        if name_to_check in current_names:
            raise KeyError("Team name {} is already in use.".format(name_to_check))
        current_names.append(name_to_check)
        current_names.sort()
        self._save_team_names()
        return name_to_check
    


    def is_name_available(self, desired_name):
        """
        Check to see if the sanitized and prettified
        version of the desired name is available (IE,
        if it's not already in use).

        If the desired name is available, return
        { "teamname": CLEANNAME, # sanitized and prettified
          "available": "yes",
        }
        If the desired name is already in use, return
        { "teamname": CLEANNAME, # sanitized and prettified
          "available": "no",
        }
        """
        if desired_name is None:
            raise ValueError('No name supplied')
        clean_name = desired_name.strip()
        clean_name = self._sanitize_name(clean_name)
        clean_name = self._prettify_name(clean_name)
        if self.current_names is None:
            raise ValueError('Cannot read current team names')
        retDict = { 'teamname': clean_name }
        if clean_name in self.current_names:
            retDict['available'] = 'no'
        else:
            retDict['available'] = 'yes'
        return retDict
            

        
    def get_single_name(self, new_name):
        """
        
        Sanitize and prettify new_name, then,
        if it exists in the current list of team names,
        return the sanitized and prettified version.
        If it doesn't exist, return empty string.
        
        """
        if new_name is None:
            raise ValueError('No name supplied')
        new_name = new_name.strip()
        new_name = self._sanitize_name(new_name)
        new_name = self._prettify_name(new_name)
        if self.current_names is None:
            raise ValueError('Cannot read current team names')
        
        if new_name in self.current_names:
            return new_name
        else:
            return ''
      
    def submit_add_team_form(self, form_data):
        """
        Make a call to the Jotform /form/{id}/submissions/
        endpoint. (http://api.jotform.com/docs/#post-form-id-submissions)
        On success return submission id.
        On failure return None
        """
        retValue = None
        response = self.readWriteClient.create_form_submission(ADD_TEAM_FORM_ID, form_data)
        if response:
            retValue = response.get('submissionID', None)
        return retValue
