###############################################################################
# Copyright 2014-2015 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's ADRC Forms project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Run a test-suite with multiple browsers using
dynamic code based on data in the `actors/xyz/actor.json` file.

@author: Andrei Sura
"""

import unittest
import argparse
import sys
import logging
from selenium import webdriver

import browser_type
from driver_manager import DriverManager
from configurable_test_case_params import ConfigurableTestCaseParams
from configurable_test_case import ConfigurableTestCase

from forms.form_a1_test import FormA1Test
from forms.form_a2_test import FormA2Test
from forms.form_a3_test import FormA3Test
from forms.form_a4_test import FormA4Test
from forms.form_a5_test import FormA5Test
from forms.form_b1_test import FormB1Test
from forms.form_b2_test import FormB2Test
from forms.form_b3_test import FormB3Test
from forms.form_b4_test import FormB4Test
from forms.form_b5_test import FormB5Test
from forms.form_b5s_test import FormB5sTest
from forms.form_b6_test import FormB6Test
from forms.form_b6s_test import FormB6sTest
from forms.form_b7_test import FormB7Test
from forms.form_b7s_test import FormB7sTest
from forms.form_b8_test import FormB8Test
from forms.form_b9_test import FormB9Test
from forms.form_c1_test import FormC1Test
from forms.form_c1s_test import FormC1sTest
from forms.form_d1_test import FormD1Test
from forms.form_e1_test import FormE1Test
from forms.form_z1_test import FormZ1Test

# set unittest logging (by default logs nothing)
logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

default_url = 'http://localhost:8081/redcap/redcap_v6.0.5/ProjectSetup/index.php?pid=12'
default_username = ''
default_password = 'secret'

def main():
    """
    Implements test suite access point
    """
    parser = argparse.ArgumentParser()
    default_actor = '../actors/recall_kent/actor.json'
    parser.add_argument('-d', '--ds_file',
            default=default_actor,
            help="Path to the json file to use for the test")
    parser.add_argument('-b', '--browsers',
            default=browser_type.BROWSER_TYPE_PHANTOMJS,
            help="[phantomjs,firefox,chrome,safari] Comma-separate browser names")
    parser.add_argument('-c', '--check',
            default=False, action='store_true',
            help="Boolean flag to enable data checks after saving a form")
    parser.add_argument('-v', '--verbosity',
           default=1, type=int,
           help="[ 3|2|1|0 ] Verbosity level (debug | info | warning | none)")
    parser.add_argument('-a', '--address',
           default=default_url,
           help="The url of the target site to test ({}".format(default_url))
    parser.add_argument('-u', '--username',
           default='',
           help="The username used to login to the target website ({}".format(default_username))
    parser.add_argument('-p', '--password',
           default='',
           help="The password used to login to the target website ({}".format(default_password))


    args = parser.parse_args()

    # same url is used by all test instances
    ConfigurableTestCase.set_proj_url(args.address)
    data = ConfigurableTestCase.parse_data_source(args.ds_file)
    actor_id = data['actor_id']

    logger.level = logging.ERROR

    if args.verbosity == 1:
        # https://docs.python.org/2/library/logging.html
        logger.level = logging.WARNING
    elif args.verbosity == 2:
        logger.level = logging.INFO
    elif args.verbosity == 3:
        logger.level = logging.DEBUG

    browser_names = args.browsers.split(',')
    logger.warn("# Selected browsers: {}".format(browser_names))
    logger.warn("# Selected actor: {}".format(args.ds_file))
    DriverManager.configure(browser_names)

    tests = [
        FormA1Test, FormA2Test, FormA3Test, FormA4Test, FormA5Test,
        FormB1Test, FormB2Test, FormB3Test, FormB4Test, FormB5Test, FormB5sTest,
        FormB6Test, FormB6sTest, FormB7Test, FormB7sTest, FormB8Test, FormB9Test,
        FormC1Test, FormC1sTest, FormD1Test, FormE1Test, FormZ1Test
        ]

    #tests = [FormA1Test]
    #tests = [FormA3Test]

    for selected_browser in DriverManager.browsers:
        logger.debug("\n#==> Executing the test suite with: '{}' browser".format(selected_browser))
        driver = DriverManager.get_driver(selected_browser)

        if args.username:
            # perform login using username/password
            ConfigurableTestCase.loginto_project(driver, args.username, args.password)

        ConfigurableTestCase.goto_project(driver)
        ConfigurableTestCase.add_actor(driver, actor_id)
        suite = unittest.TestSuite()

        # add all tests to be executed
        for test in tests:
            actor_form_data = test.get_actor_form_data(data)
            params = ConfigurableTestCaseParams(driver, actor_form_data, args)
            suite.addTest(ConfigurableTestCase.add_params(test, params=params))

        # run the tests
        unittest.TextTestRunner(verbosity=0).run(suite)
        #ConfigurableTestCase.delete_actor(driver, actor_id)
        driver.quit()

if __name__ == '__main__':
    main()
