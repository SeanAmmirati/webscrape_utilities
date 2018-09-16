from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import yaml
import sys
from helpers import create_abs_path


class WebDriverUtil(object):
    def __init__(self):
        # Initializes arguments in config file
        conf_path = create_abs_path(__file__, '../conf/config.yaml')
        argdict = yaml.load(open(conf_path, 'rb'))
        for arg, key in argdict.items():
            setattr(self, arg, key)
        driver_path = create_abs_path(__file__, self.PATH_TO_DRIVER)
        self.driver = webdriver.Chrome(driver_path)

    def access_website(self, website):
        self.driver.get(website)

    def search_google(self, term):
        self.driver.get('https://www.google.com')
        search_bar = self.driver.find_element_by_name('q')
        search_bar.send_keys(term)
        search_bar.send_keys(Keys.RETURN)

    def open_top_n_results(self, term, n=1):
        self.search_google(term)
        links = list(self.driver.find_elements_by_class_name('r'))
        print(links)
        for link in links[0: n]:
            url = link.find_element_by_css_selector('a').get_attribute('href')
            self.driver.get(url)

if __name__ == '__main__':
    wbd = WebDriverUtil()
    wbd.search_google('Hello World')
    wbd.open_top_n_results('Hello World', 1)
