###############################################################################
# Copyright 2014-2015 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's ADRC Forms project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Helper class for choosing a proper driver when running
ConfigurableTestCase tests.

@see suite.py#main()

@author: Andrei Sura
"""

from selenium import webdriver
from browser_type import BROWSER_TYPE_PHANTOMJS
from browser_type import BROWSER_TYPE_FIREFOX
from browser_type import BROWSER_TYPE_CHROME
from browser_type import BROWSER_TYPE_SAFARI
from browser_type import BROWSER_TYPE_OPERA
from browser_type import BROWSER_TYPE_ANDROID

class DriverManager:
    """
    Initially the list of browsers is empty.
    A call to #configure() method is used to add
    a browser and the corresponding driver to the `drivers` dictionary.
    """
    browsers = []
    drivers = {}

    valid_browsers = [
        BROWSER_TYPE_PHANTOMJS,
        BROWSER_TYPE_FIREFOX,
        BROWSER_TYPE_CHROME,
        BROWSER_TYPE_SAFARI,
        #BROWSER_TYPE_OPERA,
        #BROWSER_TYPE_ANDROID,
        ]

    @classmethod
    def configure(self, browser_names):
        for browser in browser_names:
            assert browser in self.valid_browsers
            self.browsers.append(browser)

        browsers = self.browsers
        self.drivers = {
            BROWSER_TYPE_PHANTOMJS: webdriver.PhantomJS() if BROWSER_TYPE_PHANTOMJS in browsers else None,
            BROWSER_TYPE_FIREFOX:   webdriver.Firefox()   if BROWSER_TYPE_FIREFOX in browsers else None,
            BROWSER_TYPE_CHROME:    webdriver.Chrome()    if BROWSER_TYPE_CHROME in browsers else None,
            BROWSER_TYPE_SAFARI:    webdriver.Safari()    if BROWSER_TYPE_SAFARI in browsers else None,
            BROWSER_TYPE_OPERA:     webdriver.Opera()     if BROWSER_TYPE_OPERA in browsers else None,
            BROWSER_TYPE_ANDROID:   webdriver.Android()   if BROWSER_TYPE_ANDROID in browsers else None,
        }

    @classmethod
    def get_driver(self, browser_name):
        """
        Use this method to selecte a proper driver for a specified browser
        """
        assert browser_name in self.valid_browsers
        driver = self.drivers[browser_name]
        #driver.set_window_size(1024, 768)
        driver.implicitly_wait(4)
        return driver
