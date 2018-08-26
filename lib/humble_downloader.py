# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 14:04:02 2018

@author: Sean
"""

from webdriver import WebDriverUtil

class HumbleBundleHelper(WebDriverUtil):
    def __init__(self):
        super(HumbleBundleHelper, self).__init__()

    def login_to_humble(self):
        self.access_website('https://www.humblebundle.com')
        login_class = self.humble['HUMBLE_LOGIN_CLASS']
        login_button =  self.find_elements_by_class_name(login_class)
        login_button.click()