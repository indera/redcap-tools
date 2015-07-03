###############################################################################
# Copyright 2014-2015 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's ADRC Forms project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

# Helper script for executing common tasks for ADRC tests
#
# @author: Andrei Sura

ACTOR_JSON := '../actors/recall_kent/actor.json'
SAND_URL := 'http://localhost:8081/redcap/redcap_v6.0.5/ProjectSetup/index.php?pid=12'
PROD_URL := 'https://redcap.ctsi.ufl.edu/redcap/redcap_v6.0.5/ProjectSetup/index.php?pid=1527'
STAG_URL := 'https://redcapstage.ctsi.ufl.edu/redcap/redcap_v6.0.5/ProjectSetup/index.php?pid=808'

REDCAP_URL := $(STAG_URL)

help:
	@echo "Available tasks:"
	@echo " test               : run the test suite against the local vagrant box using phantomjs"
	@echo " test_ff            : run the test suite against the local vagrant box using firefox"
	@echo " test_ch            : run the test suite against the local vagrant box using chrome"
	@echo " test_sa            : run the test suite against the local vagrant box using safari"

	@echo " test_ctsi_ph       : run the test suite against redcap.ctsi.ufl.edu using phantomjs"
	@echo " test_ctsi_ff       : run the test suite against redcap.ctsi.ufl.edu using firefox"
	@echo " test_ctsi_ch       : run the test suite against redcap.ctsi.ufl.edu using chrome"
	@echo " test_ctsi_sa       : run the test suite against redcap.ctsi.ufl.edu using safari"

	@echo " clean              : remove unnecessary files"

test:
	python suite.py -d $(ACTOR_JSON) --address $(SAND_URL) -c -v 1
test_ff:
	python suite.py -d $(ACTOR_JSON) --address $(SAND_URL) -c -v 1 -b firefox
test_ch:
	python suite.py -d $(ACTOR_JSON) --address $(SAND_URL) -c -v 1 -b chrome
test_sa:
	python suite.py -d $(ACTOR_JSON) --address $(SAND_URL) -c -v 1 -b safari


test_ctsi_ph:
	python suite.py -d $(ACTOR_JSON) --address $(REDCAP_URL) -v 1 -c -u $(REDCAP_ENV_USERNAME) -p $(REDCAP_ENV_PASSWORD)
test_ctsi_ff:
	python suite.py -d $(ACTOR_JSON) --address $(REDCAP_URL) -v 1 -c -u $(REDCAP_ENV_USERNAME) -p $(REDCAP_ENV_PASSWORD) --browser=firefox
test_ctsi_ch:
	python suite.py -d $(ACTOR_JSON) --address $(REDCAP_URL) -v 1 -c -u $(REDCAP_ENV_USERNAME) -p $(REDCAP_ENV_PASSWORD) --browser=chrome
test_ctsi_sa:
	python suite.py -d $(ACTOR_JSON) --address $(REDCAP_URL) -v 1 -c -u $(REDCAP_ENV_USERNAME) -p $(REDCAP_ENV_PASSWORD) --browser=safari


kill_selenium:
	echo -e `ps  | grep selenium | cut -d ' ' -f11` | kill

clean:
	find ./ -name \*.pyc | xargs rm -f
	rm -f ghostdriver.log


