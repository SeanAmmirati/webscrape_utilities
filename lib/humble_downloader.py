
"""
Created on Sat Aug 25 14:04:02 2018

@author: Sean
"""
from time import sleep

import yaml

from helpers import create_abs_path
from outlook_utility import OutlookEmailUtility
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver import WebDriverUtil


class HumbleBundleHelper(WebDriverUtil):
    """
    A Utility to sign into Humble Bundle and download specific files.

    Attributes
    ----------
    HUMBLE: dict
        A dictionary containing the relevant arguments to the Humble Bundle website.
        Relevant attributes are contained in the YAML file at config.yaml.
    OUTLOOK: dict
        A dictionary containing the relevant arguments to searching for Outlook email.
        Relevant attributes are contained in the YAML file at config.yaml.
    CAPTCHA_WAIT_TIME: int
        Number of seconds to wait to solve Captcha (must be done by user).
    """

    def __init__(self):
        """Inherits from WebDriver class to use Selenium.
        """
        super(HumbleBundleHelper, self).__init__()

    def login_to_humble(self, login, password):
        """
        Logs into HumbleBundle with supplied login and password.

        Parameters
        ----------
        login : str
            Login user information to Humble Bundle (an email address)
        password : str
            Login password
        """
        self.access_website(self.HUMBLE['URL'])
        LOGIN_CLASS = self.HUMBLE['LOGIN_LOC']
        login_button = self.driver.find_element(By.XPATH, LOGIN_CLASS)
        login_button.click()
        email_entry = self.driver.find_element_by_name('username')
        email_entry.send_keys(login)
        password_entry = self.driver.find_element_by_name('password')
        password_entry.send_keys(password)
        email_entry.send_keys(Keys.RETURN)

    def solving_captcha(self):
        """Waits a specified number of seconds before continuing for CAPTCHA.

        """
        sleep(self.CAPTCHA_WAIT_TIME)

    def find_outlook_code(self, search_depth):
        """Finds validation code sent by utilizing Outlook.

        Parameters
        ----------
        search_depth : int
            How many emails to search for Humble Bundle email? Too long may include
            old validation files, while too short may miss it.

        """
        SUBJECT_SEARCH = self.HUMBLE['SUBJECT_SEARCH']
        BODY_SEARCH = self.HUMBLE['BODY_SEARCH']

        outlook = OutlookEmailUtility(**self.OUTLOOK)
        email_body = outlook.search_email_subject(SUBJECT_SEARCH).values()
        code = outlook.search_email_body(search_term=BODY_SEARCH,
                                         body=str(email_body),
                                         grp_num='code')
        return code

    def enter_code(self, code):
        pass


if __name__ == '__main__':
    secrets_file = create_abs_path(__file__, '../conf/secrets.yaml')
    login_info = yaml.load(open(secrets_file))['sign_in']
    login = login_info['email_address']
    password = login_info['password']

    try:
        browser = HumbleBundleHelper()
        browser.login_to_humble(login, password)
        print(browser.find_outlook_code(3))
    except Exception as e:
        print(e)
        browser.driver.close()
