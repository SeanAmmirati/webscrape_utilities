# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 22:18:25 2018

@author: Sean
"""

import win32com.client as win_client
import itertools
import yaml 
import re

class OutlookEmailUtility(object):
    def __init__(self, CONFIG_PATH = None, CONFIG_KEY = None, **kwargs):
        if not CONFIG_PATH or CONFIG_KEY:
            CONFIG_PATH = '../conf/config.yaml'
            CONFIG_KEY = 'outlook'
        
        if not kwargs: 
            kwargs = yaml.load(open(CONFIG_PATH))[CONFIG_KEY]
        for k, v in kwargs.items():
            setattr(self, k, v)
            
        outlook = win_client.Dispatch(self.APPLICATION_NAME)\
                                     .GetNamespace(self.NAMESPACE_NAME)
        self.inbox = outlook.GetDefaultFolder(self.DEFAULT_FOLDER).Items
    
    def search_email_subject(self, search_term):
        self.search_results = {}
        
        for email in itertools.islice(reversed(self.inbox), self.SEARCH_DEPTH):
            if re.match(search_term, email.Subject, re.IGNORECASE) is not None:
                self.search_results[email.Subject] = email.Body
        
        return self.search_results
    
    def search_email_body(self, search_term, body, grp_num=0):
        return re.search(search_term, body, re.IGNORECASE).group(grp_num)