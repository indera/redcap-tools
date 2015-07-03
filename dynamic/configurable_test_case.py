###############################################################################
# Copyright 2014-2015 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's ADRC Forms project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Base class for tests that require parameters.
@see suite#main()

@author: Andrei Sura
"""
import unittest
import json
import time
import collections
import argparse
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import UnexpectedAlertPresentException

from action import Action
from forms.config import naming
from configurable_test_case_params import ConfigurableTestCaseParams
from action_statistic import ActionStatistic

logger = logging.getLogger(__name__)


class ConfigurableTestCase(unittest.TestCase):

    project_url = ''
    @classmethod
    def get_actor_form_data(cls, data):
        """ Find the dictionary specific to an actor=>form """
        # naming = { 'FormA1Test' : { 'name': "a1_subject_demographics" ...
        actor_form_index = naming[cls.__name__]['name']
        return data['actor_data'][actor_form_index]


    @classmethod
    def set_proj_url(cls, url):
        cls.project_url = url


    @classmethod
    def get_proj_url(cls):
        """ The project url is set from the command line """
        return cls.project_url


    def get_form_url(self):
        """
        @see #goto_form_longitudinal()

        @TODO: pass actor id to the instance and the event_id for each form
        (can use xpath
         "//a[contains(@href, 'id=actor_kent_recall')]/@href"
            DataEntry/index.php?pid=34&amp;id=actor_kent_recall&amp;event_id=382&amp;page=z1_form_checklist
        )
        """
        # http://localhost:8081/redcap/redcap_v6.0.5/ProjectSetup/index.php?pid=12
        # redcap/redcap_v6.0.5/DataEntry/index.php?pid=34&id=1&event_id=382&page=z1_form_checklist
        url = ConfigurableTestCase.get_proj_url()
        url = url.replace("ProjectSetup", "DataEntry")

        actor_id = "actor_kent_recall"
        event_id = 382
        form_name = naming[self.get_class_name()]['name']
        url += "&id={}&page={}&event_id={}".format(actor_id, form_name, event_id)
        # //*[@id="form[a1_subject_demographics]"]
        # xpath = "//a[@id='form[{}]')]".format(name)
        print "using form_url:" + url
        return url


    def __init__(self, methodName='runTest', params=None):
        """
        Add hook for attaching extra parameters
        Parameter:
            driver: WebDriver object to be used
            data: the dictionary with actor information
        """
        super(ConfigurableTestCase, self).__init__(methodName)
        self.driver = params.driver
        self.data = params.data
        self.do_check = params.do_check
        logger.debug("Using data: {}".format(self.data))

    def setUp(self):
        self.verificationErrors = []
        self.accept_next_alert = True

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

    def get_driver():
        return self.driver

    def get_class_name(self):
        return self.__class__.__name__

    def get_display_name(self):
        return naming[self.get_class_name()]['display_name']

    def goto_form(self):
        """
        Click on a data collection instrument name
        when the project *is not* longitudinal
        """
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        display_name = naming[self.get_class_name()]['display_name']
        xpath = "//a[contains(text(), '{}')]".format(display_name)
        ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        ele.click()

        logger.warn("""\n# goto form: {} """.format(display_name))
        logger.info("""wait = WebDriverWait(driver, 10)""")
        logger.info("""xpath = "{}" """.format(xpath))
        logger.info("""ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))""")
        logger.info("""ele.click()""")


    def goto_form_longitudinal(self):
        """
        Click on a data collection instrument event 1
        when the project *is* longitudinal
        """
        url = self.get_form_url()
        self.driver.get(url)


    def save_form(self):
        """ Click the 'Save' button for a form """
        logger.warn("""# save data for form '{}'""".format(self.get_display_name()))
        xpath = "//input[@name='submit-btn-savecontinue']"
        ConfigurableTestCase.click_ele(self.driver, xpath)


    def run_test(self):
        """"
        Use selenium to open the proper form and start entering the data.
        Note: This function is called by every child class.

        @TODO: improve exception handling for longitudinal projects
        """
        try:
            # self.goto_form()
            self.goto_form_longitudinal()

            stat = ActionStatistic(self.get_class_name())

            # for every field enter data as needed...
            for action_data in self.data:
                action = Action(self.driver, action_data)
                success = action.execute()
                stat.update(action, success)
                #time.sleep(0.5) # uncomment for debugging in the browser

            logger.warning(stat.to_string())
            self.save_form()

            # for every field check if the value was saved properly...
            if self.do_check:
                logger.info("""\n# Perform data integrity check for form: {}""".format(self.get_display_name()))
                for action_data in self.data:
                    action = Action(self.driver, action_data)
                    action.check_result()

        except UnexpectedAlertPresentException:
            alert = self.driver.switch_to_alert()
            alert.accept()
            logger.warning("skip UnexpectedAlertPresentException {} for {}".format(alert.text, type(self)))


    @staticmethod
    def add_params(configurable_class, params):
        """
        Classes extending ConfigurableTestCase can access
        extra parameters directly as:
            print self.driver, self.data
        """
        loader = unittest.TestLoader()
        tests = loader.getTestCaseNames(configurable_class)
        suite = unittest.TestSuite()

        for test in tests:
            suite.addTest(configurable_class(test, params=params))

        return suite


    @staticmethod
    def parse_data_source(ds_file):
        """
        Translate the `actor json file` into a dictionary
        Parameters
        ----------
        ds_file : string
            The name of the file
        return : dict
            The parsed dictionary
        """
        with open(ds_file) as f:
            data = f.read()
            js_obj = json.loads(data)
            #ordered = collections.OrderedDict(sorted(js_obj['xyz'].items()))
            return js_obj


    @staticmethod
    def send_keys(driver, xpath, keys):
        wait = WebDriverWait(driver, 10)
        ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        ele.send_keys(keys)

    @staticmethod
    def click_ele(driver, xpath):
        wait = WebDriverWait(driver, 10)
        ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        ele.click()


    @staticmethod
    def loginto_project(driver, username, password):
        #url = ConfigurableTestCase.get_login_url()
        url = 'https://redcap.ctsi.ufl.edu/redcap'
        logger.warn("# goto login url: {}".format(url))
        driver.get(url)

        ConfigurableTestCase.send_keys(driver, "//input[@id='username']", username)
        ConfigurableTestCase.send_keys(driver, "//input[@id='password']", password)
        ConfigurableTestCase.click_ele(driver, "//input[@name='login']")


    @staticmethod
    def goto_project(driver):
        """ Not an instance method because we call it before creating an instance"""
        url = ConfigurableTestCase.get_proj_url()
        logger.warn("# goto project url: {}".format(url))
        driver.get(url)


    @staticmethod
    def add_actor(driver, actor_id):
        """
        Insert a new subject for which we need to insert data
        @see #delete_actor()
        """
        wait = WebDriverWait(driver, 10)
        xpath = "//a[contains(text(),'Add / Edit Records')]"
        ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        ele.click()

        xpath = "//input[@id='inputString']"
        ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        ele.clear()
        ele.send_keys(actor_id)
        ele.send_keys(Keys.ENTER)
        time.sleep(0.5)

        logger.warn("\n# Add actor: {}".format(actor_id))
        logger.info('driver.get("{}")'.format(ConfigurableTestCase.get_proj_url()))
        logger.info("""wait = WebDriverWait(driver, 10)""")
        logger.info("""xpath = "//a[contains(text(),'Add / Edit Records')]" """)
        logger.info("""ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))""")
        logger.info("""ele.click()""")

        logger.info("""xpath = "//input[@id='inputString']" """)
        logger.info("""ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))""")
        logger.info("""ele.send_keys("{}")""".format(actor_id))
        logger.info("""ele.send_keys(Keys.ENTER)""")
        logger.info("""time.sleep(0.5)""")


    @staticmethod
    def delete_actor(driver, actor_id):
        """
        Remove the data for the specified actor_id.
        @TODO: For longitudinal projects there is no "Delete" button
        visible when selecting a record (since there are events)

        @see #add_actor()
        """
        logger.warn("# delete actor: '{}'".format(actor_id))
        wait = WebDriverWait(driver, 10)
        xpath = "//a[contains(text(),'Add / Edit Records')]"
        ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        ele.click()
        time.sleep(0.5)

        xpath = "//input[@id='inputString']"
        ele = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        ele.clear()
        ele.send_keys(actor_id)
        ele.send_keys(Keys.ENTER)
        time.sleep(0.5)

        driver.find_element_by_xpath("//input[@name='submit-btn-delete']").click()
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
