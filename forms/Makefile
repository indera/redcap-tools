###############################################################################
# Copyright 2014-2015 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's ADRC Forms project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

# Helper script for merging/uploading/downloading metadata files UDS v3
#
# @author: Andrei Sura
# @TODO: update test targets for ivp & mfvp


# Define variable defaults
MAKE_CONFIG_FILE := Makefile.ini
REDCAP_URL := http://localhost:8998/redcap
REDCAP_VERSION := 6.0.5
PROJECT_ID := 12
API_TOKEN := PLEASE_SPECIFY_ONE_IN_MAKEFILE_INI

# To properly define the variables please create a Makefile.ini (see Makefile.ini.example)
ifneq ("$(wildcard $(MAKE_CONFIG_FILE))", "")
	include $(MAKE_CONFIG_FILE)
   REDCAP_URL := $(shell cat ${MAKE_CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'redcap_url=' | cut -d '=' -f2)
   REDCAP_VERSION := $(shell cat ${MAKE_CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'redcap_version=' | cut -d '=' -f2)
   PROJECT_ID := $(shell cat ${MAKE_CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'project_id=' | cut -d '=' -f2)
   API_TOKEN := $(shell cat ${MAKE_CONFIG_FILE} | sed -e 's/ //g' | grep -v '^\#' | grep 'api_token=' | cut -d '=' -f2)
endif

# Use variables
API_CALL           := curl -s -X POST $(REDCAP_URL)/api/ -d token=$(API_TOKEN) -d content=metadata -d format=csv
API_CALL_META_XML  := curl -s -X POST $(REDCAP_URL)/api/ -d token=$(API_TOKEN) -d content=metadata -d format=xml
API_CALL_META_JSON := curl -s -X POST $(REDCAP_URL)/api/ -d token=$(API_TOKEN) -d content=metadata -d format=json

API_CALL_RECORD_CSV  := curl -s -X POST $(REDCAP_URL)/api/ -d token=$(API_TOKEN) -d content=record -d format=csv
API_CALL_RECORD_JSON := curl -s -X POST $(REDCAP_URL)/api/ -d token=$(API_TOKEN) -d content=record -d format=json
API_CALL_RECORD_XML  := curl -s -X POST $(REDCAP_URL)/api/ -d token=$(API_TOKEN) -d content=record -d format=xml
REDCAP_PROJECT_URL := $(REDCAP_URL)/redcap_v$(REDCAP_VERSION)/ProjectSetup/index.php?pid=$(PROJECT_ID)
UPLOAD_CALL := python ../scripts/upload_data_dictionary.py $(REDCAP_PROJECT_URL)


ACTOR_JSON := '../tests/actors/recall_kent/actor_v2.json'
ACTOR_TEST_RUNNER := python ../tests/dynamic/suite.py -d $(ACTOR_JSON) --address $(REDCAP_PROJECT_URL) -c -v 1


help:
	@echo "Available tasks:"

	@echo "\t get_ivp_one:           Download one IVP form by specifying: a1, a2...'"
	@echo "\t get_mfvp_one:          Download one MFVP form by specifying: m1, m2...'"
	@echo "\t merge_ivp:             concatenate all IVP forms into one 'data-dictionary.csv'"
	@echo "\t upload_ivp:            upload the IVP 'data-dictionary.csv' (uses phantomjs)"
	@echo "\t upload_ivp_one:        upload the specified IVP: a1, a2, ... (uses phantomjs)"
	@echo "\t upload_ivp_firefox:    upload the IVP 'data-dictionary.csv' (uses firefox)"

	@echo "\t merge_all:             concatenate v2 IVP and Miami FVP forms into one 'data-dictionary.csv'"
	@echo "\t upload_all:            upload the v2 IVP and Miami FVP forms (uses phantomjs)"
	@echo "\t upload_all_firefox:    upload the v2 IVP and Miami FVP forms (uses firefox)"

	@echo "\t test:                  execute selenium tests for all forms using phantomjs"
	@echo "\t test_old:              execute selenium tests for all forms using old tests"
	@echo "\t pretty:                download data dictionary and format it for readability"
	@echo "\t get_all:               download metadata for all forms in csv format"
	@echo "\t get_all_xml:           download metadata for all forms in xml format"
	@echo "\t get_all_json:          download metadata for all forms in json format"

	@# Tasks for inspecting the project structure: Arms, Instruments, Instrument-Event Mapping
	@echo "\t get_arms:              download the list of ARMs in a longitudinal project"
	@echo "\t get_instruments:       download the list of instruments (aka forms) in a longitudinal project"
	@echo "\t get_events:            download the list of events in a longitudinal project (a comma separated list of ARMS can be specified)"
	@echo "\t get_mapping_evt_inst:  download the mapping of events to instruments in a longitudinal project (a comma separated list of ARMS can be specified)"
	@echo "\t inspect:               run the tasks that give insights about the longitudinal project structure"
	@echo "\t show_tables:           show the list of tables in the REDCap database"
	@echo "\t show_events_info:      show event_ids in the REDCap database"


upload_ivp_one:
	@# Note: provide the form name as: z1, a1...
	$(eval FORM_FILE := ivp_2008/form_$($(filter-out $@,$(MAKECMDGOALS))).csv)
	@test -f $(FORM_FILE) || (echo 'The specified file "$(FORM_FILE)" does not exist' && exit 1)
	@echo "Uploading file: $(FORM_FILE)"
	$(UPLOAD_CALL) $(FORM_FILE)

upload_mfvp_one:
	@# Note: provide the form name as: m1, m2...
	$(eval FORM_FILE := mfvp_$(filter-out $@,$(MAKECMDGOALS)).csv)
	@test -f $(FORM_FILE) || (echo 'The specified file "$(FORM_FILE)" does not exist' && exit 1)
	@echo "Uploading file: $(FORM_FILE)"
	$(UPLOAD_CALL) $(FORM_FILE)


merge_ivp:
	rm -f data-dictionary.csv
	cat ivp_z1.csv > data-dictionary.csv
	awk 'FNR>2' `find . -regex '\./ivp_[a-y].*\.csv'` >> data-dictionary.csv

upload_ivp:
	make merge_ivp
	$(UPLOAD_CALL) data-dictionary.csv
upload_ivp_firefox:
	make merge_ivp
	$(UPLOAD_CALL) data-dictionary.csv -s

merge_all:
	rm -f data-dictionary.csv
	cat ivp_2008/form_z1*.csv > data-dictionary.csv
	awk 'FNR>2' `find ./ivp_2008 -regex '\./ivp_2008/form_[a-y].*\.csv'` >> data-dictionary.csv
	awk 'FNR>2' `find . -regex '\./mfvp_[a-z].*\.csv'` >> data-dictionary.csv

upload_all:
	make merge_all
	$(UPLOAD_CALL) data-dictionary.csv
upload_all_firefox:
	make merge_ivp_mfvp
	$(UPLOAD_CALL) data-dictionary.csv -s

get_all:
	@$(API_CALL) -d forms[]=

get_arms:
	@# arm_num, name
	@#       1, "Arm 1"
	@$(API_CALL) -d content=arm

get_instruments:
	@# instrument_name      ,        instrument_label
	@# ivp_z1_form_checklist, "Ivp Z1 Form Checklist"
	@$(API_CALL) -d content=instrument

get_events:
	@# event_name, arm_num, day_offset, offset_min, offset_max, unique_event_name
	@# "Event 1",         1,          0,          0,          0,   "event_1_arm_1"
	@$(eval ARMS := $(filter-out $@,$(MAKECMDGOALS)))
	@$(API_CALL) -d content=event -d arms=$(ARMS)

get_mapping_evt_inst:
	@# make get_event_mapping 1
	@$(eval ARMS := $(filter-out $@,$(MAKECMDGOALS)))
	@$(API_CALL) -d content=formEventMapping -d arms=$(ARMS)

inspect:
	make get_arms | column -s, -t
	make get_instruments | column -s, -t
	make get_events | column -s, -t
	make get_mapping_evt_inst | column -s, -t

show_tables:
	VAGRANT_CWD=~/git/vagrant-redcap vagrant ssh -c 'mysql -uredcap -ppassword -e "show tables from redcap;" '

show_events_info:
	$(eval STATS_SQL := $(shell cat stats.sql))
	VAGRANT_CWD=~/git/vagrant-redcap vagrant ssh -c 'mysql -uredcap -ppassword -e "$(STATS_SQL)" '

get_ivp_one:
	@$(eval FORM := $($(filter-out $@,$(MAKECMDGOALS))))
	@$(API_CALL) -d forms[]=$(FORM)

get_mfvp_one:
	@$(eval FORM := $($(filter-out $@,$(MAKECMDGOALS))))
	@$(API_CALL) -d forms[]=$(FORM)

get_ivp:
	@# Download all form metadata if no argument is specified
	@# Note: Variables a1, a2 ... need to be defined in Makefile.ini
	@$(eval FORMS := -d forms[]=$(z1))
	@$(eval FORMS += -d forms[]=$(a1))
	@$(eval FORMS += -d forms[]=$(a2))
	@$(eval FORMS += -d forms[]=$(a3))
	@$(eval FORMS += -d forms[]=$(a4))
	@$(eval FORMS += -d forms[]=$(a5))
	@$(eval FORMS += -d forms[]=$(b1))
	@$(eval FORMS += -d forms[]=$(b2))
	@$(eval FORMS += -d forms[]=$(b3))
	@$(eval FORMS += -d forms[]=$(b4))
	@$(eval FORMS += -d forms[]=$(b5))
	@$(eval FORMS += -d forms[]=$(b5s))
	@$(eval FORMS += -d forms[]=$(b6))
	@$(eval FORMS += -d forms[]=$(b6s))
	@$(eval FORMS += -d forms[]=$(b7))
	@$(eval FORMS += -d forms[]=$(b7s))
	@$(eval FORMS += -d forms[]=$(b8))
	@$(eval FORMS += -d forms[]=$(b9))
	@$(eval FORMS += -d forms[]=$(c1))
	@$(eval FORMS += -d forms[]=$(c1s))
	@$(eval FORMS += -d forms[]=$(c2))
	@$(eval FORMS += -d forms[]=$(d1))
	@$(eval FORMS += -d forms[]=$(e1))
	echo "printing $(FORMS)"
	$(API_CALL) $(FORMS)

get_ivp_one_xml:
	@$(eval FORM := $($(filter-out $@,$(MAKECMDGOALS))))
	$(API_CALL_META_XML) -d forms[]=$(FORM) | xmlstarlet fo

get_all_json:
	@$(API_CALL_META_JSON) | python -m json.tool
get_all_json_groupped:
	@$(API_CALL_META_JSON) -d groupByForm=1 | python -m json.tool
get_all_json_numbered:
	@$(API_CALL_META_JSON) | python -m json.tool | grep field_name | cut -d : -f 2 | nl


get_stats_fields:
	@echo "The number of variables by type:"
	@make get_all_json | grep field_type | sed -s "s/ //g" | sort | uniq -c | sort -r
get_stats_branching_logic:
	@echo "The number of variables with branching logic is:"
	@ make get_all_json  | grep branching_logic | grep -v '"branching_logic": ""' | wc -l


read_csvdata:
	@$(API_CALL_RECORD_CSV) -d records=a1_1
read_xmldata:
	@$(API_CALL_READ_XML) -d records=a1_1 | xmlstarlet fo
read_jsondata:
	@$(API_CALL_READ_JSON) -d records=a1_1 | python -m json.tool


read_csvdata_a1:
	@#$(API_CALL_RECORD_CSV) -d forms[]=a1_subject_demographics -d records=a1_1 -type=eav
	@$(API_CALL_RECORD_CSV) -d forms[]=ivp_a1_subject_demographics -d records=a1_1 -type=flat
read_xmldata_a1:
	@$(API_CALL_RECORD_XML) -d forms[]=ivp_a1_subject_demographics -d records=a1_1 | xmlstarlet fo
read_jsondata_a1:
	@$(API_CALL_RECORD_JSON) -d forms[]=ivp_a1_subject_demographics -d records=a1_1 | python -m json.tool

write_csvdata_a1:
	@#$(API_CALL_RECORD_CSV) -d data=@a1_1.csv -d type=eav
	$(API_CALL_RECORD_CSV) -d data=@a1_1.csv -d type=flat
write_xmldata_a1:
	@#$(API_CALL_RECORD_XML) -d data=@a1_1_eav.xml -d type=eav
	$(API_CALL_RECORD_XML) -d data=@a1_1.xml -d type=flat
write_jsondata_a1:
	@#$(API_CALL_RECORD_JSON) -d data=@a1_1.json -d type=eav
	$(API_CALL_RECORD_JSON) -d data=@a1_1.json -d type=flat


pretty:
	@# TODO: update to work for any form
	make get_all | column -s, -t | nl | less


test_old:
	for i in ../tests/form_*.py; do echo "Execute: python $$i" && python $$i; done

test:
	$(ACTOR_TEST_RUNNER)
test_ff:
	$(ACTOR_TEST_RUNNER) -b firefox
test_ch:
	$(ACTOR_TEST_RUNNER) -b chrome
test_sa:
	$(ACTOR_TEST_RUNNER) -b safari



test_repeat:
	for i in {1..2}; do make test; done

clean:
	rm -f data-dictionary.csv
	rm -f screenshot-timeout.png
	rm -f ghostdriver.log
