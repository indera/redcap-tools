###############################################################################
# Copyright 2014-2015 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's ADRC Forms project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Utility class for storing configuration data for ConfigurableTestCase class.

@author: Andrei Sura
"""

class ConfigurableTestCaseParams(object):

    def __init__(self, driver, data, args):
        self.driver = driver
        self.data = data
        self.do_check = args.check
