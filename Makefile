# Helper script for executing common tasks for the longitudinal project
#
# @author: Andrei Sura
#
# TODO: add support for selecting a browser

VERBOSITY := 2

SAND_URL := 'http://127.0.0.1:8081/redcap/index.php'
STAG_URL := 'https://redcapstage.ctsi.ufl.edu/redcap/index.php'
PROD_URL := 'https://redcap.ctsi.ufl.edu/redcap/index.php'
REDCAP_URL := $(SAND_URL)
#REDCAP_URL := $(STAG_URL)
#REDCAP_URL := $(PROD_URL)

META_FILE          := 'forms/data-dictionary.csv'
JSON_SETTINGS      := 'scripts/longitudinal_settings_v2.json'
CRED_FILE          := ~/longitudinal_credentials

RUNNER     := 'scripts/longitudinal.py'
EXE_RUNNER := python $(RUNNER) -m $(META_FILE) -s $(JSON_SETTINGS) -v $(VERBOSITY) --url $(REDCAP_URL) -p -b chrome

help:
	@echo "Available tasks:"
	@echo "\t deploy                 : Create a project with multiple events on $(SAND_URL) using $(JSON_SETTINGS)"
	@echo "\t deploy_with_login      : Create a project with multiple events on $(REDCAP_URL) using $(JSON_SETTINGS)"

check_meta:
	@test -f $(META_FILE) \
		|| ( \
			echo 'Please create the $(META_FILE) file by merging csv files in the "forms" folder ' \
			&& echo 'You can merge the files by executing:' \
			&& echo "\t pushd forms && make merge_all && popd" \
			&& exit 1)


deploy: check_meta
	$(EXE_RUNNER)

deploy_with_login: check_meta
	$(EXE_RUNNER) -c $(CRED_FILE)

merge:
	bash scripts/merge-forms.bash
