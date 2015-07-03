#!/usr/bin/env python
###############################################################################
# Copyright 2014-2015 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's ADRC Forms project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Implement Taeber's idea about parsing NACC data dictionaries into REDCap metdata

@author: Andrei Sura
"""

import csv
import os
import sys
import re
import logging
import argparse

from converter_config import naming
from converter_config import NACC_DATA_TYPES

# @TODO: make a dedicated class NaccRow to simplify field parsing
from converter_config import COL_0_ITEM_NUM, COL_1_DATA_ORDER, COL_2_DATA_ELE, COL_3_FORM_VER
from converter_config import COL_4_FORM_PACKET, COL_5_FORM_ID, COL_6_UDS_QUESTION
from converter_config import COL_7_DATA_TYPE, COL_8_DATA_LEN, COL_09_COL1, COL_10_COL2, COL_11_RANGE1, COL_12_RANGE2
from converter_config import COL_MISS_BEGIN, COL_MISS_END
from converter_config import COL_VAL_BEGIN, COL_VAL_END
from converter_config import COL_VALD_BEGIN, COL_VALD_END
from converter_config import COL_BLANKS_BEGIN, COL_BLANKS_END

logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

FORMS_ALL = 'all'
PACKET_IVP = 'ivp'
PACKET_FVP = 'fvp'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--packet',
            default=PACKET_IVP,
            help="[ivp | fvp] The forms packet to convert")
    parser.add_argument('-f', '--forms',
            default=FORMS_ALL,
            help="[a1,a2,...]")
    parser.add_argument('-v', '--verbosity',
           default=1, type=int,
           help="[ 3|2|1|0 ] Verbosity level (debug | info | warning | none)")

    args = parser.parse_args()
    logger.level = logging.ERROR

    if args.verbosity == 1:
        logger.level = logging.WARNING
    elif args.verbosity == 2:
        logger.level = logging.INFO
    elif args.verbosity == 3:
        logger.level = logging.DEBUG

    packet = args.packet
    logger.info("# Parsing forms for {} packet".format(packet))
    naming_dict = naming[packet]
    section_header_1 = """<h2>
<span style='background: #000; color: #fff; padding: 3px;'>{}</span> NACC UNIFORM DATA SET (UDS)
</h2>
<h1>
Form {}: {}
</h1>
INSTRUCTIONS:{}
"""
    form_count = 0
    specified_forms = args.forms.split(',')

    for form in naming_dict:
        if FORMS_ALL != args.forms:
            # convert specific forms only
            if form not in specified_forms:
                logger.warn("Skipping conversion for form: {}".format(form))
                continue

        form_count += 1
        f = os.path.join("dict_{}".format(packet), naming_dict[form]['file'])
        form_name = naming_dict[form]['name'] # Example: z1_form_checklist
        form_name_u = form.upper() # Example: Z1

        # Apply the convention for form naming
        metadata_form_name = Row.get_metadata_form_name(packet, form_name) # Example: ivp_z1_form_checklist
        form_descr = naming_dict[form]['descr']
        form_instr = naming_dict[form]['instr']
        packet_description = naming["{}_extra".format(packet)]['title']

        # @TODO: extract logic into Row.get_metadata_form_header()
        section_header_form = section_header_1.format(packet_description, form_name_u, form_descr, form_instr)
        meta = Row.get_metdata_first_line(packet)

        with open (f, 'rb') as csvfile:
            logger.info("# ==> Parsing input file: {}".format(f))
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            line_num = 0

            # loop through the lines of the original data dictionary
            for row in reader:
                line_num += 1
                if 1 == line_num:
                    # skip the dictionary header line
                    continue

                row_obj = Row(packet, form, row)
                variable_number = row[COL_0_ITEM_NUM].strip().lower()
                variable = row[COL_2_DATA_ELE].strip().lower()
                section_header = section_header_form if (2 == line_num) else ""
                metadata_question_label = row_obj.get_metadata_question_label()
                # Apply the convention for variable naming
                metadata_variable_name = Row.get_metadata_variable_name(packet, form, variable_number, variable)

                # @TODO:re-use the row_obj
                choices_list = get_answer_choices(packet, form, row)
                select_choices_or_calculations = "|".join(choices_list)
                logger.debug("{} choices: {}".format(metadata_variable_name, select_choices_or_calculations))
                field_note = "" #row[COL_7_DATA_TYPE]
                text_validation_type_or_show_slider_number = ""
                text_validation_min = ""
                text_validation_max = ""
                identifier = ""
                branching_logic = row_obj.show_rule.to_string()
                required_field = ""
                custom_alignment = ""
                question_number = ""
                matrix_group_name = ""

                meta += '"{}",'.format(metadata_variable_name)
                meta += '"{}",'.format(metadata_form_name)
                meta += '"{}",'.format(section_header)
                meta += '"{}",'.format(get_field_type(row, choices_list))
                meta += '"{}",'.format(metadata_question_label)
                meta += '"{}",'.format(select_choices_or_calculations)
                meta += '"{}",'.format(field_note)
                meta += '"{}",'.format(text_validation_type_or_show_slider_number)
                meta += '"{}",'.format(text_validation_min)
                meta += '"{}",'.format(text_validation_max)
                meta += '"{}",'.format(identifier)
                meta += '"{}",'.format(branching_logic)
                meta += '"{}",'.format(required_field)
                meta += '"{}",'.format(custom_alignment)
                meta += '"{}",'.format(question_number)
                meta += '"{}"'.format(matrix_group_name)
                meta += "\n"

            # All rows parsed, save the file (ivp_a1.csv, fvp_a1.csv, ...)
            dest_file = os.path.join('../forms/', "{}_{}.csv".format(packet, form))
            with open(dest_file, 'wb')  as dest:
                dest.write(meta)
                logger.info("#  Saved {} form to file: {}".format(form, dest_file))

    logger.info("# Parsed {} forms".format(form_count))


def is_empty(val):
    """
    Helper for finding non-empty values.
    Note: space-only strings or '.' are considered `empty`
    """
    return val in ['.', '']

def has_value(row):
    has = False

    for i in range(COL_VAL_BEGIN, COL_VAL_END):
        val = row[i].strip()

        if not is_empty(val):
            logger.debug("Found value: {} at index {} in row {}".format(val, i, row))
            has = True
            break

    return has


def is_first_val_empty_but_second_nonempty(row):
    missing_val = row[COL_MISS_BEGIN].strip()
    val1 = row[COL_VALD_BEGIN].strip()
    val2 = row[COL_VALD_BEGIN + 1].strip()
    return is_empty(val1) and not is_empty(val2) and not is_empty(missing_val)

def is_identical_miss1_val1_val2(row):
    """
    Helper method to detect error in dictionary and skip
    """
    miss1 = row[COL_MISS_BEGIN].strip()
    miss2 = row[COL_MISS_BEGIN + 1].strip()
    val1 = row[COL_VALD_BEGIN].strip()
    val2 = row[COL_VALD_BEGIN + 1].strip()
    return not is_empty(miss1) and miss1 == val1 and miss1 == val2


def get_count_for_values_in_missing_columns(row):
    count = 0

    for i in range(COL_MISS_BEGIN, COL_MISS_END):
        val = row[i].strip()

        if not is_empty(val):
            count += 1

    return count 


def has_values_in_missing_columns(row):
    """
    @see
    """
    return get_count_for_values_in_missing_columns(row) > 0

def has_one_value_in_missing_columns(row):
    """
    If a row has just one extra value in the `MISS1` column
    the use the `VALD2` as a displayed option.
    @see 
    """
    return get_count_for_values_in_missing_columns(row) == 1

def is_numeric(row):
    return 'Num' == row[COL_7_DATA_TYPE].strip()

def is_numeric_with_unknown(row):
    return 'Num_with_unknown' == row[COL_7_DATA_TYPE].strip()


def get_field_type(row, answer_choices):
    """
    For some fields the data type is dropdown
    @see: #get_answer_choices()
    """
    nacc_data_type = row[COL_7_DATA_TYPE].strip()

    #if is_numeric_with_unknown(row): return 'text'

    if is_numeric(row):
        if not has_value(row) or len(answer_choices) > 20:
            return 'dropdown'

    return NACC_DATA_TYPES[nacc_data_type]


def get_min_max(answer_choices):
    """
    @TODO: change the `answer_choices` data structure so it is possible to extract the min/max values
    """
    if answer_choices:
        #return answer_choices[0]
        return (1, 2)

    return None


def get_answer_choices(packet, form, row):
    """
    Generate the specially formated string for options
    Example: "1, University of Florida | 2, Mount Sinai"

    @see #has_one_value_in_missing_columns()
    @aww #is_empty()
    ----------
    Parameters:
        :row dictionary
        :return list
    """
    data_type = get_field_type(row, [])

    if 'text' == data_type:
        return ''

    ele_number = row[COL_0_ITEM_NUM].strip().lower()
    ele = row[COL_2_DATA_ELE].strip().lower()
    choices = []

    debug_id = Row.get_metadata_variable_name(packet, form, ele_number, ele)
    # logger.debug(debug_id)
    range_begin = int(row[COL_11_RANGE1])
    range_end   = int(row[COL_12_RANGE2])
    missing_val = row[COL_MISS_BEGIN].strip()
    missing_choice = row[COL_VALD_BEGIN + 1].strip()
    number_of_vals_in_missing_columns = get_count_for_values_in_missing_columns(row)

    logger.debug("{} range: {} to {}".format(debug_id, range_begin, range_end))

    #if has_values_in_missing_columns(row):
    #    logger.debug("has_values_in_missing_columns: {}".format(number_of_vals_in_missing_columns))
    #    # Special case like (FVP C2 5a): range 0-14, Miss1 = 95, Miss2 = 96, Miss3 = 97, Miss4 = 98
    #    # Number Span Test Forward -  Number of correct trials
    #    # Need to show options 0-14 and 95-98
    #    for i in range(0, number_of_vals_in_missing_columns):
    #        val = row[COL_MISS_BEGIN + i]
    #        choice = "{} - {}".format(val, row[COL_VALD_BEGIN + 1 + i])
    #        logger.info("Adding range values and missing values for {}: {} - {}".format(debug_id, val, choice))
    #        choices.append('{}, {}'.format(val, choice))

    #    for i in range(range_begin, range_end + 1):
    #        logger.info("Adding range values and missing values for {}: {} - {}".format(debug_id, i, i))
    #        #val = row[COL_VALD_BEGIN + i] if row[COL_VALD_BEGIN + i] else i
    #        choices.append('{}, {}'.format(i, i))

    #elif not has_value(row):
    #    # use the range values to define options
    #    if range_begin >= 0:
    #        if has_one_value_in_missing_columns(row):
    #            logger.info("Add single missing choice for {}: {} - {}".format(debug_id, missing_val, missing_choice))
    #            choices.append('{}, {}'.format(missing_val, missing_choice))

    #        for i in range(range_begin, range_end + 1):
    #            logger.debug("Add range choice for {}: {}".format(debug_id, i))
    #            choices.append('{}, {}'.format(i, i))
    #    else:
    #        logger.error("Unexpected error for: {}".format(debug_id))
    #else:
    #    logger.debug("Choice generate last case for: {}".format(debug_id))
    #    for i in range(COL_VAL_BEGIN, COL_VAL_END):
    #        val = row[i].strip()
    #        display_choice = row[i+12].strip()
    #        logger.debug("val:{}|".format(val))

    #        if val not in ['.', ''] and display_choice not in ['.', '']:
    #            logger.debug("{} choice: {}".format(debug_id, display_choice))
    #            choices.append('{},{} '.format(val, display_choice))
    #        else:
    #            logger.debug("Skip choice for {} value: {}".format(debug_id, val))

    logger.debug("Add choice for general case: {}".format(debug_id))
    is_identical_123 = is_identical_miss1_val1_val2(row)
    i = 0

    for val_index in range(COL_VAL_BEGIN, COL_VAL_END+1):
        if is_first_val_empty_but_second_nonempty(row) or is_identical_123:
            # do not add any values due `numeric with unknow` special case
            continue

        i += 1
        val = row[val_index].strip()
        val_label = row[val_index + 12].strip()
        choice = '{},{} '.format(val, val_label)
        logger.debug("val:{}|".format(val))

        if not is_empty(val) and not is_empty(val_label) and choice not in (choices):
            logger.debug("{} has proper val and choice: {}".format(debug_id, choice))
            choices.append(choice)

    if not choices:
        if is_first_val_empty_but_second_nonempty(row):
            logger.info("Add single missing choice for {}: {} - {}".format(debug_id, missing_val, missing_choice))
            choices.append('{}, {}'.format(missing_val, missing_choice))

        logger.debug("Trying to add range choices for: {}".format(debug_id))

        if range_begin >= 0:
            for i in range(range_begin, range_end + 1):
                range_choice = '{}, {}'.format(i, i)
                if range_choice in choices:
                    continue

                logger.debug("Add range choice for {}: {}".format(debug_id, i))
                choices.append(range_choice)

    if not choices:
        logger.debug("Unable to produce valid choices for {}".format(debug_id))
        sys.exit()

    return choices

class Row(object):
    """
    Helper class used for data dictionary parsing
    @see #get_branching_logic()
    """
    def __init__(self, packet, form, row):
        self.row            = row
        self.packet         = packet
        self.form           = form
        self.ele_num        = row[COL_0_ITEM_NUM].strip().lower()
        self.ele            = row[COL_2_DATA_ELE].strip().lower()
        self.question       = row[COL_6_UDS_QUESTION].strip()
        self.data_type      = row[COL_7_DATA_TYPE].strip()
        self.debug_id       = Row.get_metadata_variable_name(self.packet, self.form, self.ele_num, self.ele)

        # "Blank" comes from the input data dictionary terminology
        self.blank_rules    = [ row[i].strip() for i in range(COL_BLANKS_BEGIN, COL_BLANKS_END)]

        # "Show" comes from the terminology used in REDCap form metadata files
        self.show_rule      = Rule(self.packet, self.form, Row.extract_rules(self))


    def get_metadata_question_label(self,):
        return "{}. {}".format(self.ele_num, self.question)


    @staticmethod
    def get_metdata_first_line(packet):
        """
        For forms part of the same project there should be only one field as identifier according to REDCap,
        therefore the 'FVP' forms use the same identifier variable as IVP: `ivp_z1_0e_ptid`
        """
        return """field_name,form_name,section_header,field_type,field_label,select_choices_or_calculations,field_note,text_validation_type_or_show_slider_number,text_validation_min,text_validation_max,identifier,branching_logic,required_field,custom_alignment,question_number,matrix_group_name
"ivp_z1_0e_ptid","{}_z1_form_checklist","","text","Subject ID","","","","","","","","Y","","",""
""".format(packet)

    @staticmethod
    def get_metadata_variable_name(packet, form, ele_num, ele):
        return "{}_{}_{}_{}".format(packet, form, ele_num, ele)


    @staticmethod
    def get_metadata_form_name(packet, form_name):
        return "{}_{}".format(packet, form_name)

    @staticmethod
    def extract_rules(row):
        """
        :row Row
            The instance object to be parsed
        """
        rules = []

        for br in row.blank_rules:
            if br:
                rules.append(br)
            else:
                logger.debug("Skip rule parsing for: {}".format(row.debug_id))

        return rules

class Rule(object):
    """
    Abstractization for branching logic
    """
    matcher_or = re.compile(r"^(Blank if Question)\s{0,}(\w+)\s{0,}(\w+)\s{0,}(=|ne)\s{0,}(\w+).*")
    matcher_and= re.compile(r"^(#)(\w+) (\w+) (=|ne) (\w+).*")

    check_values = {
        '=': '<>',
        'ne': '=',
    }

    def __init__(self, packet, form, text_pieces):
        self.text_pieces = text_pieces
        self.or_list = []
        self.and_list = []

        for txt in self.text_pieces:
            logger.debug("{} - {}".format(form, txt))

            pieces = txt.split(' and ')

            if len(pieces) > 1:
                for p in pieces:
                    m = Rule.matcher_and.match(p)
                    if not m:
                        continue

                    var_number = m.group(2).strip().lower()
                    var_name   = m.group(3).strip().lower()
                    check_type = Rule.check_values[m.group(4).strip().lower()]
                    check_value = m.group(5).strip().lower()
                    metadata_variable_name = Row.get_metadata_variable_name(packet, form, var_number, var_name)
                    #self.and_list.append("[{}_{}_{}_{}] {} '{}'".format(packet, form, var_number, var_name, check_type, check_value))
                    self.and_list.append("[{}] {} '{}'".format(metadata_variable_name, check_type, check_value))

            else:
                try:
                    m = Rule.matcher_or.match(txt)
                    var_number = m.group(2).strip().lower()
                    var_name   = m.group(3).strip().lower()
                    check_type = Rule.check_values[m.group(4).strip().lower()]
                    check_value= m.group(5).strip().lower()
                    metadata_variable_name = Row.get_metadata_variable_name(packet, form, var_number, var_name)
                    #self.or_list.append("[{}_{}_{}_{}] {} '{}'".format(packet, form, var_number, var_name, check_type, check_value))
                    self.or_list.append("[{}] {} '{}'".format(metadata_variable_name, check_type, check_value))
                except Exception as e:
                    logger.error("Form '{}' error: Unable to parse branching logic: '{}'".format(form, txt))


    def to_string(self):
        """
        Apply De'Morgan rule to convert
        "Blank if a || b..." into "Show the field ONLY if... not a && not b"
        """
        logger.debug(self.text_pieces)

        if self.or_list:
            logger.debug("OR conditions: {} ".format(self.or_list))
            return " AND ".join(self.or_list)

        logger.debug("AND conditions: {} ".format(self.and_list))
        return " OR ".join(self.and_list)

    @staticmethod
    def parse(rule_text):
        return


if __name__ == '__main__':
    main()
