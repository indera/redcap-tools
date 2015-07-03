###############################################################################
# Copyright 2014-2015 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's ADRC Forms project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################


"""
Implement different `actions` depending on `field type`

@author: Andrei Sura
"""
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import logging
logger = logging.getLogger(__name__)

class Action(unittest.TestCase):
    FIELD_TYPE_RADIO = 'radio'
    FIELD_TYPE_TEXT = 'text'
    FIELD_TYPE_DROPDOWN = 'dropdown'
    FIELD_TYPE_CHECKBOX = 'checkbox'

    def __init__(self, driver, action_data):
        self.driver = driver
        self.label  = action_data['data_1_label'].encode('utf-8')
        choices = action_data['data_2_choices'].encode('utf-8')
        logger.debug("Parsing {} choices: {} ".format(action_data['field_name'], choices))
        self.choices    = Action.parse_choices(choices)
        self.answer     = action_data['data_3_answer']
        self.story      = action_data['data_4_story']
        self.logic      = action_data['data_5_logic']
        self.fname      = action_data['field_name']
        self.ftype      = action_data['field_type']

    @staticmethod
    def parse_choices(choices_string):
        # Obtain a dictionary from strings like "1, Yes | 0, No"
        valid_choices = dict()

        if not '|' in choices_string:
            return valid_choices

        # use an index for options
        index = 1

        for choice in choices_string.split('|'):
            key, val = choice.split(',', 1)
            valid_choices[key.strip()] = { 'index': index, 'value': val.strip() }
            index += 1

        logger.debug("valid_choices: {}".format(valid_choices))
        return valid_choices


    def execute(self):
        """
        Data-driver dispatcher for different action types

        :return False if the action was not executed, True otherwise
        """
        driver = self.driver

        # @TODO: move the `ifs` into dedicated objects
        if not self.answer:
            return False

        wait = WebDriverWait(driver, 10)

        if Action.FIELD_TYPE_RADIO == self.ftype:
            html_ele_index = self.choices[self.answer]['index']
            xpath = "(//input[@name='{}___radio'])[{}]".format(self.fname, html_ele_index)
            logger.debug("# waith for ele: {}".format(xpath))
            ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            ele.click()

            logger.info("""html_ele_index = "{}" """.format(html_ele_index))
            logger.info("""xpath = "(//input[@name='{}___radio'])[{}]" """.format(self.fname, html_ele_index))
            logger.info("""ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))""")
            logger.info("""ele.click()""")

        elif Action.FIELD_TYPE_TEXT == self.ftype:
            xpath = "//input[@name='{}']".format(self.fname)
            logger.debug("# waith for ele: {}".format(xpath))
            ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            ele.clear()
            ele.send_keys(self.answer)
            ele.send_keys(Keys.TAB)

            logger.info("""xpath = "//input[@name='{}']" """.format(self.fname))
            logger.info("""ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))""")
            logger.info("""ele.clear()""")
            logger.info("""ele.send_keys("{}")""".format(self.answer))
            logger.info("""ele.send_keys(Keys.TAB)""")

        elif Action.FIELD_TYPE_DROPDOWN == self.ftype:
            ele = driver.find_element_by_xpath("//select[@name='{}']".format(self.fname))
            drop_down_value = self.choices[self.answer]['value']
            (Select(ele)).select_by_visible_text(drop_down_value)

            logger.info("""ele = driver.find_element_by_xpath("//select[@name='{}']\")""".format(self.fname))
            logger.info("""# Select drop_down_value: \"{}\" """.format(self.choices[self.answer]['value']))
            logger.info("""(Select(ele)).select_by_visible_text(drop_down_value)""")

        elif Action.FIELD_TYPE_CHECKBOX == self.ftype:
            html_ele_index = self.choices[self.answer]['index']
            xpath = "(//input[@name='__chkn__{}'])[{}]".format(self.fname, html_ele_index)
            ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            ele.click()

            logger.info("driver.find_element_by_xpath(\"//input[@name='__chkn__{0}'])[{1}]\").click() \t\t # answer: ({2})"
                .format(self.fname, html_ele_index, self.answer))

        else:
            raise Exception("# Action not implemented for variable '{}'".format(self.fname))

        return True

    def check_result(self):
        """
        Check if the data for a specific field was saved
        @see http://selenium-python.readthedocs.org/en/latest/api.html
        """
        if not self.answer:
            return
        driver = self.driver

        logger.debug("# {} ==> check value: {} ".format(self.label, self.answer))

        if Action.FIELD_TYPE_RADIO == self.ftype:
            html_ele_index = self.choices[self.answer]['index']
            ele = driver.find_element_by_xpath(
                "(//input[@name='{}___radio'])[{}]".format(self.fname, html_ele_index))
            self.assertTrue(ele.is_selected())

            logger.info("""ele = driver.find_element_by_xpath(\"//input[@name='{0}']\") \t# answer: {1}"""
                .format(self.fname, self.answer))
            logger.info("""self.assertTrue(ele.is_selected())""")

        elif Action.FIELD_TYPE_TEXT == self.ftype:
            ele = driver.find_element_by_xpath("//input[@name='{}']".format(self.fname))
            actual_value = ele.get_attribute('value')
            logger.debug("""# Actual value: {}, expected value: {}""".format(actual_value, self.answer))
            self.assertTrue(self.answer == ele.get_attribute('value'))

            logger.info("""ele = driver.find_element_by_xpath("//input[@name='{}']") \t# answer: {}""".format(self.fname, self.answer))
            logger.info("""self.assertTrue("{}" == ele.get_attribute('value'))""".format(self.answer))

        elif Action.FIELD_TYPE_DROPDOWN == self.ftype:
            ele = driver.find_element_by_xpath("//select[@name='{}']".format(self.fname))
            self.assertTrue(self.answer == ele.get_attribute('value'))

            logger.info("""ele = driver.find_element_by_xpath("//select[@name='{}']".format(self.fname))""")
            logger.info("""self.assertTrue(self.answer == ele.get_attribute('value'))""")

        elif Action.FIELD_TYPE_CHECKBOX == self.ftype:
            html_ele_index = self.choices[self.answer]['index']
            ele = driver.find_element_by_xpath(
                "(//input[@name='__chkn__{}'])[{}]".format(self.fname, html_ele_index))
            self.assertTrue(ele.is_selected())

            logger.info("driver.find_element_by_xpath(\"//input[@name='__chkn__{0}'])[{1}]\").click() \t\t # answer: ({2})"
                .format(self.fname, html_ele_index, self.answer))
            logger.info("""self.assertTrue(ele.is_selected())""")

        else:
            raise Exception("# Action not implemented for variable '{}'".format(self.fname))


    def check_logic(self):
        #TODO: Verify the branching logic
        #ele.is_displayed()
        pass
