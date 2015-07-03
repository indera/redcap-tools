#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright 2014-2015 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's toolbox. 
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Helper classes for create-long-project.py

Note: Some tips about REDCap forms can be found at
    http://redcapinfo.ucdenver.edu/index.php?option=com_content&view=article&id=62&Itemid=74

@author: Andrei Sura
"""

import os.path
import logging
import collections
import json
import time
import pprint
import pickle
import datetime
from urlparse import parse_qs, urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

# This sets the number of seconds the driver
# will wait for slow operations to complete
# (increase to make the software more resilient to server loads)
DEFAULT_WAIT = 10
PROJECT_PURPOSE_PRACTICE = 'Practice / Just for fun'
PROJECT_PURPOSE_OPERATIONAL = 'Operational Support'
PROJECT_PURPOSE_RESEARCH = 'Research'
PROJECT_PURPOSE_QUALITY_IMPROVEMENT = 'Quality Improvement'
PROJECT_PURPOSE_OTHER = 'Other'
PROJECT_PURPOSE_OTHER_SPECIFY = 'Other Purpose'

PROJECT_INFO_FILE = 'project.info'

class ProjectCreatorParams(object):
    """
    Plain old storage class
    """
    def __init__(self, url, version, projectname, username, password, metadata):
        self.url = url
        self.version = version
        self.projectname = projectname
        self.username = username
        self.password = password
        self.metadata = metadata


class ProjectCreator(object):

    def __init__(self, driver, params):
        self.driver = driver
        self.url = params.url
        self.version = params.version

        # Dictionary for keeping track of mapped events
        self.mapped_events = {}

        url_data = urlparse(params.url)
        self.url_versioned = "{}://{}/redcap/redcap_v{}".format(url_data.scheme, url_data.netloc, params.version)
        self.projectname = params.projectname
        self.username = params.username
        self.password = params.password
        self.metadata = params.metadata
        self.api_key = ''
        logger.info("Initiated project manager with url: {}".format(self.url))

    def get_api_key(self):
        return self.api_key

    def load_json_settings(self, settings_file):
        """
        Load the event-form mapping configuration data from a separate json file.

        @see #map_instruments_to_events()
        """
        with open(settings_file) as f:
            data = f.read()
            js_obj = json.loads(data)
            self.settings = js_obj['settings']
            self.sorted_events = {}

            # sort the events to undo lexicographic ordering
            for k, v in self.settings['events_list'].iteritems():
                self.sorted_events[int(k)] = v

            logger.info("Loaded settings from file: {}".format(settings_file))
            logger.debug("Settings: {}".format(self.sorted_events))


    def get_project_id(self):
        """
        Warning: this function reads properly the project id
            only after the project was created and the driver was not redirected
            to a page outside the scope of the project.

        @see create_project()
        """
        url = self.driver.current_url
        qs_data = parse_qs(urlparse(url).query, keep_blank_values=True)
        pid = [int(i) for i in qs_data['pid']][0]
        return pid


    def type_ele(self, xpath, keys):
        """
        Emulates a user typing a string (the input is cleared first)
        """
        wait = WebDriverWait(self.driver, DEFAULT_WAIT)
        ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        ele.clear()
        ele.send_keys(keys)

    def type_ele_no_clear(self, xpath, keys):
        """
        Emulates a user typing a string
        """
        wait = WebDriverWait(self.driver, DEFAULT_WAIT)
        ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        ele.send_keys(keys)


    def click_ele(self, xpath):
        """
        Emulates a user clicking an element on the page
        """
        wait = WebDriverWait(self.driver, DEFAULT_WAIT)
        ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        ele.click()


    def select_ele(self, xpath, text):
        """
        Emulates a user selecting an element in a drop-down element on the page
        """
        wait = WebDriverWait(self.driver, DEFAULT_WAIT)
        ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        Select(ele).select_by_visible_text(text)

    def wait_until_ele_visible(self, xpath):
        """
        An expectation for checking that an element is present on the DOM of a page and visible.
        http://selenium.googlecode.com/git/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html
        """
        wait = WebDriverWait(self.driver, DEFAULT_WAIT)
        ele = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))


    def loginto_project(self):
        """
        For production/staging servers we need to provide credentials to login
        before creating a project.

        Note: This function expects the url for the login page to be provided
        in the settings *.json file.

        @see #load_json_settings()
        """
        if not self.username:
            logger.warn("No username specified. Skip login.")
            return

        url = self.url
        logger.warn("# goto login url: {}".format(url))
        self.driver.get(url)
        self.type_ele_no_clear("//input[@id='username']", self.username)
        self.type_ele_no_clear("//input[@id='password']", self.password + Keys.ENTER)
        # self.click_ele("//input[@name='login']")
        # results = wait.until(lambda driver: self.driver.find_element_by_id('g'))
        self.wait_until_ele_visible("//img[contains(@src, 'redcaplogo.gif')]")


    def goto_redcap(self):
        self.driver.get(self.url)

    def get_url_create_project(self):
        return "{}?action=create".format(self.url)

    def get_url_project_setup(self):
        #http://127.0.0.1:8081/redcap/redcap_v6.0.5/ProjectSetup/index.php?pid=12
        return "{}/ProjectSetup/index.php?pid={}".format(self.url_versioned, self.projectid)

    def get_url_api(self):
        return "{}/API/project_api.php?pid={}".format(self.url_versioned, self.projectid)

    def get_url_upload_data_dictionary(self):
        return "{}/Design/data_dictionary_upload.php?pid={}".format(self.url_versioned, self.projectid)

    def get_url_define_events(self):
        #http://127.0.0.1:8081/redcap/redcap_v6.0.5/Design/define_events.php?pid=12
        return "{}/Design/define_events.php?pid={}".format(self.url_versioned, self.projectid)

    def get_url_designate_instruments(self):
        return "{}/Design/designate_forms.php?pid={}".format(self.url_versioned, self.projectid)

    def get_url_add_record(self):
        return "{}/DataEntry/grid.php?pid={}".format(self.url_versioned, self.projectid)

    def get_url_status_dashboard(self):
        return "{}/DataEntry/record_status_dashboard.php?pid={}".format(self.url_versioned, self.projectid)


    def create_project(self):
        """
        Emulates an user entering all data necessary for a project creation
        """
        url = self.get_url_create_project()
        logger.info("Creating project '{}' on page: {} with metdata file: {}"
                .format(self.projectname, url, self.metadata))
        self.driver.get(url)
        self.click_ele("//input[@id='app_title']")
        self.type_ele("//input[@id='app_title']", self.projectname)

        # @TODO: should this be a class attribute?
        project_purpose = PROJECT_PURPOSE_RESEARCH
        self.select_ele("//select[@id='purpose']", project_purpose)

        if PROJECT_PURPOSE_OTHER == project_purpose:
            self.type_ele("//*[@id='purpose_other_text']", PROJECT_PURPOSE_OTHER_SPECIFY)
            self.click_ele("//input[@value=' Create Project ']")

        elif PROJECT_PURPOSE_RESEARCH == project_purpose:
            # When the purpose is `Research` an extra checkbox is required: `Area of research`
            self.click_ele("//input[@id='purpose_other[7]']")
            self.click_ele("//input[@value=' Create Project ']")
            try:
                # confirm warning...
                self.click_ele("//span[@class='ui-button-text'][text() = 'I Agree']")
            except:
                logger.warn("There was no confirmation window when creating the project")

        # Set as longitudinal
        self.click_ele("//button[@id='setupLongiBtn']")
        self.projectid = self.get_project_id()


    def create_api_key(self):
        """
        Note: after creation the API KEY the web page displays it
        so we save it in a class variable.

        @TODO: save the key to a file?
        Warning: PhantomJS might require tweaking to work (http://docs.seleniumhq.org/docs/03_webdriver.jsp#popup-dialogs)
        """
        driver = self.driver
        url = self.get_url_api()
        logger.info("Creating API key on page: {}".format(url))
        driver.get(url)
        self.click_ele("//div[@id='apiReqBoxId']/button")

        try:
            # Wait until the API options dialog is visible
            self.wait_until_ele_visible("//span[@id='ui-dialog-title-rightsDialogId']")

            """
            driver.find_element_by_id("api_export").click()
            driver.find_element_by_id("api_import").click()
            driver.find_element_by_id("api_send_email").click()
            """

            # Make the API KEY to support both import and export functions
            self.click_ele("//*[@id='api_export']")
            self.click_ele("//*[@id='api_import']")
            # un-check the "Send-email" box to prevent failures
            self.click_ele("//*[@id='api_send_email']")

            # click "Create new API token"
            self.click_ele("(//button[@type='button'])[2]")

            # Go back to the `API` page to read the key created
            driver.get(self.get_url_api())
            self.api_key = self.driver.find_element_by_id("apiTokenId").text
            logger.info("API KEY: {}".format(self.api_key))
        except TimeoutException as e:
            logger.error("Unable to complete creation of API keys: {}".format(e))


    def upload_metadata(self):
        """
        Emulates an user uploading a metadata file from the local machine.
        xpath('.//div[@class="darkgreen"]/b[1][text()]')

        Copied from Taeber's `upload_data_dictionary.py`
        """
        url = self.get_url_upload_data_dictionary()
        logger.info("Uploading metadata file {} on page: {}".format(self.metadata, url))
        logger.info("Metadata file last modified: {}" .format(ProjectCreator.modification_date(self.metadata)))
        self.driver.get(url)
        #self.type_ele("//*[@name='uploadedfile']", self.metadata)
        self.driver.find_element_by_name('uploadedfile').send_keys(self.metadata)

        time.sleep(0.1)
        self.click_ele("//input[@id='submit']")
        time.sleep(0.1)
        #self.click_ele("//input[@name='commit']")
        assert "Your document was uploaded successfully and awaits your confirmation below." == \
               self.driver.find_element_by_css_selector("div.darkgreen > b").text
        self.driver.find_element_by_name("commit").click()
        assert "Changes Made Successfully!" == self.driver.find_element_by_css_selector("div.green > b").text
        logger.info("Upload completed")


    def create_events(self):
        """
        Selenium is used because REDCap API does not contain any functions
        for mapping the forms to events or even to create events.
        Before we crate additional events we want to store the `default event id`
        so we can delete it later if needed.
        Note: This function would be useful for inclusion in https://github.com/ctsit/redcap-extras

        @see #find_default_event_mapping()
        @see #map_instruments_to_events()
        """
        self.default_event_id = self.find_default_event_mapping()

        events_list = self.sorted_events
        days_offset = self.settings['days_offset']
        increment_offset = self.settings['increment_offset']

        logger.info("Creating {} events...".format(len(events_list)))
        self.driver.get(self.get_url_define_events())
        offset = 0

        for evt in events_list:
            logger.debug("Creating event: {}".format(evt))
            offset += increment_offset
            name = events_list[evt]['name']
            self.type_ele("//input[@id='day_offset']", days_offset)
            self.type_ele("//input[@id='offset_min']", offset)
            self.type_ele("//input[@id='offset_max']", offset)
            self.type_ele("//input[@id='descrip']", name)
            self.click_ele("//input[@id='addbutton']")


    def map_instruments_to_events(self):
        """
        This function allows to associate a form to a event.
        Currently REDCap API does not allow this kind of functionality,
        it needs to be done manually.

        @see #create_events()
        """
        logger.debug("map_instruments_to_events for project: {}".format(self.projectid))

        # Use the default event id which was set when calling #create_events()
        evt_id = self.default_event_id + 1
        self.driver.get(self.get_url_designate_instruments())
        self.click_ele("//input[@value=' Begin Editing ']")

        # For each event there is be a list of form names to map
        logger.info("Start mapping events from index: {}".format(evt_id))
        events = self.sorted_events

        for evt in events:
            if evt_id not in self.mapped_events:
                self.mapped_events[evt_id] = []

            evt_name = events[evt]['name']
            forms = events[evt]['forms']
            logger.info("# Started mapping {} forms for event '{}'".format(len(forms), evt_name))

            for form in forms:
                xpath = "//input[@id='{}--{}']".format(form, evt_id)

                try:
                    self.click_ele(xpath)
                    time.sleep(0.05)
                    logger.debug("Event '{}' was mapped to form '{}'".format(evt_name, form))
                    self.mapped_events[evt_id].append(form)
                except:
                    logger.error("Can't click: {}".format(xpath))

            # Warning: the following line assumes that the event creation happened in sequence
            # which might not be true when multiple users are creating events at the same time
            evt_id += 1

        # when done mapping click the "Save" button
        self.click_ele("//input[@id='save_btn']")


    def create_test_subject(self, subject_id):
        """
        After a project is created we can use this method to test data entry
        @TODO: test if it works properly
        """
        self.driver.get(self.get_url_add_record())
        self.type_ele("//input[@id='inputString']", subject_id + Keys.ENTER)
        self.wait_until_ele_visible("//div[@id='record_display_name']")
        logger.warn("Created test subject: {}".format(subject_id))
        time.sleep(2)


    def add_data_test_subject(self):
        # http://localhost:8081/redcap/redcap_v6.0.5/DataEntry/index.php?pid=90&id=001&event_id=476&page=ivp_z1_form_checklist
        # http://localhost:8081/redcap/redcap_v6.0.5/DataEntry/index.php?pid=90&id=001&event_id=476&page=ivp_a1_subject_demographics
        # http://localhost:8081/redcap/redcap_v6.0.5/DataEntry/index.php?pid=90&id=001&event_id=477&page=ivp_z1_form_checklist
        pass


    def delete_default_event_mapping(self):
        """
        This method deletes the default event created for the longitudinal project.
        Note: When a longitudinal project is created all forms are by default mapped to the
        event "Event 1" (which has the database id stored in `redcap_events_metadata.event_id` table.

        @see #create_events()
        @see #find_default_event_mapping()
        Warning: PhantomJS might require tweaking to work (http://docs.seleniumhq.org/docs/03_webdriver.jsp#popup-dialogs)

        :return None
        """
        self.driver.get(self.get_url_define_events())
        xpath = "//td[@id='row_a{}']/a[2]/img".format(self.default_event_id)
        logger.info("Click ele {} to delete the default event".format(xpath))

        try:
            self.click_ele(xpath)
            alert = self.driver.switch_to_alert()
            alert.accept()
        except:
            logger.error('Unexpected exception in delete_default_event_mapping()')


    def find_default_event_mapping(self):
        """"
        Helper method for #create_events()

        Note: When a longitudinal project is created all forms are by default mapped to the
        event "Event 1" (which has the database id stored in `redcap_events_metadata.event_id` table.

        The goal of this function is to find the `event_id` by `inspecting` the html
        source code since it is embedded as: td id='row_a<event_id>'
        Once the <event_id> is found it can be used for automated mapping of forms to events.

        :return int
            The value stored in `redcap_events_metadata.event_id` for the "Event 1" of the project

        @see #create_events()
        @see #map_instruments_to_events()
        """
        self.driver.get(self.get_url_define_events())
        #xpath = "//td[contains(@id, 'row_a')]/@id"
        #event_id = self.driver.find_elements_by_xpath(xpath)[0].text
        xpath = "//td[contains(@id, 'row_a')]"
        events = self.driver.find_elements_by_xpath(xpath)

        if len(events) < 1:
            raise Exception("Unable to find the event_id of the default event.")

        event = events[0].get_attribute('id')
        logger.info("Found WebElement for the first event with id: {}".format(event))
        event_id = event.split("_a")[1]
        return int(event_id)


    def delete_project(self):
        """
        Warning: this method deletes a project by ID.

        @TODO: add a flag to allow executing just this method (https://www.python.org/dev/peps/pep-0338/)
        """
        pid = self.projectid
        logger.warn("Deleting project: {}".format(pid))
        xpath = '//a[@href[contains(., "ProjectSetup/index.php?pid={}")]]'.format(pid)
        self.click_ele(xpath)
        xpath = '//a[@href[contains(., "ProjectSetup/other_functionality.php?pid={}")]]'.format(pid)
        self.click_ele(xpath)
        self.click_ele("//input[@value='Delete the project']")
        self.type_ele("//input[@id='delete_project_confirm']", 'DELETE')
        self.click_ele("(//button[@type='button'])[2]") # confirm 1
        self.click_ele("(//button[@type='button'])[4]") # confirm 2
        self.click_ele("(//button[@type='button'])[3]") # close
        time.sleep(2)


    def print_mapped_events(self):
        print("The list of events mapped:")
        pprint.pprint(self.mapped_events)


    @staticmethod
    def prompt(question, default=None):
        """
        This function prompts the user to enter a string
        when the default parameter value needs to be changed.

        Copied from Taeber's `create_project.py`
        """
        default_text = ' '
        if default:
            default_text = ' [{0}] '.format(default)
        return raw_input(question + default_text).strip() or default

    @staticmethod
    def modification_date(filename):
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)

    def save_project_info(self, project_info_file):
        pinfo = {
            'api_key': self.api_key,
            'projectid': self.projectid,
            'url_versioned': self.url_versioned,
        }
        with open(project_info_file, 'w') as f:
            pickle.dump(pinfo, f)


    @staticmethod
    def retrieve_project_info(project_info_file):
        with open(project_info_file, 'rb') as f:
            pinfo = pickle.load(f)
            pprint.pprint(pinfo)
            return pinfo


    def deploy_new_project(self):
        """
        Helper function for executing all steps for the creation of a project
        @see longitudinal#main()
        """
        pc = self
        pc.create_project()
        pc.create_api_key()
        pc.save_project_info(PROJECT_INFO_FILE)
        pc.upload_metadata()
        pc.create_events()
        pc.map_instruments_to_events()
        #pc.print_mapped_events()
        pc.delete_default_event_mapping()


    def redeploy_existing_project(self):
        """
        Helper function for uploading metdata for an existing project.

        Note: One day REDCap will provide API calls for
        creating projects and uploading metadata.

        @see longitudinal#main()
        """
        try:
            # os.path.isfile(fname)
            pinfo = ProjectCreator.retrieve_project_info(PROJECT_INFO_FILE)
            self.projectid      = pinfo['projectid']
            self.api_key        = pinfo['api_key']
            self.url_versioned  = pinfo['url_versioned']

        except IOError as e:
            logger.error("Unable to redeploy the metadata. " \
                    "No project info file found: {}".format(PROJECT_INFO_FILE))
            #raise e

        if self.projectid:
            self.upload_metadata()
        else:
            logger.error("Unable to redeploy the metadata. " \
                    "Please check if the project id is available in: {}".format(PROJECT_INFO_FILE))
