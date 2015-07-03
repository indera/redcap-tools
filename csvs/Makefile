
DIR_IVP := dict_ivp
DIR_FVP := dict_fvp

help:
	@echo "Available tasks:"
	@echo "\t convert_ivp_one  : convert a specified IVP dictionary for REDCap "
	@echo "\t convert_fvp_one  : convert a specified IVP dictionary for REDCap "

	@echo "\t convert_ivp      : convert the IVP dictionaries into 'metdatada' files for REDCap "
	@echo "\t convert_fvp      : convert the FVP dictionaries into 'metdatada' files for REDCap "
	@echo "\t get_ivp          : download csv version of Initial Visit Packet Data Dictionary files"
	@echo "\t get_fvp          : download csv version of Follow-up Visit Packet Data Dictionary files"

convert_ivp_one:
	@$(eval FORM := $(filter-out $@,$(MAKECMDGOALS)))
	python converter.py -v 3 -f $(FORM)
convert_fvp_one:
	@$(eval FORM := $(filter-out $@,$(MAKECMDGOALS)))
	python converter.py -v 3 -p fvp -f $(FORM)

convert_ivp:
	python converter.py -v 2
convert_fvp:
	python converter.py -v 2 -p fvp


get_ivp:
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedheader.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedA1IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedA2IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedA3IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedA4DIVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedA5IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB1IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB4IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB5IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB6IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB7IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB8IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB9IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedC2IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedD1IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedD2IVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedZ1IVP.csv

get_fvp:
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedheader.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedA1FVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedA2FVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedA3FVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedA4DFVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB1FVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB4FVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB5FVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB6FVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB7FVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB8FVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedB9FVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedC1FVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedC2FVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedD1FVP.csv
	wget -P $(DIR_FVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedD2FVP.csv
	wget -P $(DIR_IVP) https://www.alz.washington.edu/NONMEMBER/UDS/DOCS/VER3/uds3dedZ1FVP.csv

clean:
	rm ./$(DIR_IVP)/*
	rm ./$(DIR_FVP)/*
