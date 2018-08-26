# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 14:04:02 2018

@author: Sean
"""
import itertools
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import yaml
import win32com.client
from outlook_utility import OutlookEmailUtility
from webdriver import WebDriverUtil

class HumbleBundleHelper(WebDriverUtil):
    def __init__(self):
        super(HumbleBundleHelper, self).__init__()

    def login_to_humble(self, login, password):
        self.access_website('https://www.humblebundle.com')
        login_class = self.humble['HUMBLE_LOGIN_LOC']
        login_button =  self.driver.find_element(By.XPATH, login_class)
        login_button.click()
        email_entry = self.driver.find_element_by_name('username')
        email_entry.send_keys(login)
        password_entry = self.driver.find_element_by_name('password')
        password_entry.send_keys(password)
        email_entry.send_keys(Keys.RETURN)
        
    def solving_captcha(self):
        pass
        
    def find_outlook_code(self, search_depth):
        if 'Protection' in self.driver.title:
            BODY_SEARCH = self.humble['HUMBLE_BODY_SEARCH']
            outlook = OutlookEmailUtility(**self.outlook)
            email_body = outlook.search_email_subject('Humble.*Protection').\
                                                      values()
            import pdb; pdb.set_trace()
            code = outlook.search_email_body(search_term=BODY_SEARCH, 
                                             body=str(email_body),
                                             grp_num='code')         
            return code            
            
if __name__ == '__main__':
    login_info = yaml.load(open('../conf/secrets.yaml'))['sign_in']
    login = login_info['email_address']
    password = login_info['password']
    try:
        browser = HumbleBundleHelper()
        browser.find_outlook_code(20)
    except Exception as e:
        print(e)
        browser.driver.close()
        
    