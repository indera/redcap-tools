#!/usr/bin/env python
###############################################################################
# Copyright 2014-2015 University of Florida. All rights reserved.
# This file is part of UF CTS-IT's ADRC Forms project.
# Use of this source code is governed by the license found in the LICENSE file.
###############################################################################

"""
Configuration file for converter.py script

@author Andrei Sura
"""

NACC_DATA_TYPES = {
    'Num': 'radio',
    'Char': 'text',
}

# The numbers below represent the header row of the NACC data dictionaries
# @see `./dict_ivp` folder for an example csv
COL_0_ITEM_NUM      = 0
COL_1_DATA_ORDER    = 1
COL_2_DATA_ELE      = 2
COL_3_FORM_VER      = 3
COL_4_FORM_PACKET   = 4
COL_5_FORM_ID       = 5
COL_6_UDS_QUESTION  = 6
COL_7_DATA_TYPE     = 7
COL_8_DATA_LEN      = 8
COL_09_COL1         = 9
COL_10_COL2         = 10
COL_11_RANGE1       = 11
COL_12_RANGE2       = 12
COL_MISS_BEGIN = 13
COL_MISS_END = 18

COL_VAL_BEGIN  = 19
COL_VAL_END    = 30
COL_VALD_BEGIN = 31
COL_VALD_END   = 42
COL_BLANKS_BEGIN = 43
COL_BLANKS_END   = 47

INSTR_IVP_Z1  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by clinic staff.
</span>
NACC expects and intends that all UDS forms will be attempted on all subjects, but we realize this may be impossible
when the patient is terminally ill, or when there is no co-participant, or for other reasons. However, for a subject
to be included in the UDS database, <strong> Forms Z1, A1, A5, B4, B8, B9, C2, D1, and D2</strong> must be submitted,
even though these forms may include some items with missing data. An explanation is required below for forms that
are not submitted.

KEY: If the specified form was not completed, please enter one of the following codes:
95 = Physical problem
96 = Cognitive or behavioral problem
97 = Other problem 98=Verbal refusal

Center IDs:

2 = Boston University
3 = Case Western University 4 = Columbia University
5 = Duke University
6 = Emory University
7 = Massachusetts ADRC
8 = Indiana University
9 = Johns Hopkins University
10 = Mayo Clinic
11 = Mount Sinai
12 = New York University
13 = Northwestern University
14 = Oregon Health & Science University 15 = Rush University
16 = University of California, Davis
17 = University of California, Los Angeles 18 = University of California, San Diego
19 = University of Kentucky
20 = University of Michigan
21 = University of Pennsylvania
22 = University of Pittsburgh
25 = University of Texas Southwestern
26 = University of Washington
27 = Washington University in Saint Louis 28 = University of Alabama
30 = University of Southern California
31 = University of California, Irvine
32 = Stanford University
33 = Arizona ADC
34 = University of Arkansas
35 = University of California, San Francisco 36 = Florida ADC
37 = University of Wisconsin
38 = University of Kansas
"""

INSTR_IVP_A1  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by intake interviewer based on ADC scheduling records, subject interview, medical records,
and proxy co-participant report (as needed).
For additional clarification and examples, see UDS Coding Guidebook for Initial Visit Packet, Form A1.
</span>
"""

INSTR_IVP_A2  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by intake interviewer based on co-participant's report.
For additional clarification and examples, see UDS Coding Guidebook for Initial Visit Packet, Form A2.
</span>
"""
INSTR_IVP_A3 = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by a clinician with experience in evaluating patients with neurological problems and psychiatric conditions.
For additional clarification and examples, see UDS Coding Guidebook for Initial Visit Packet, Form A3.
</span>
"""

INSTR_IVP_A4 = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician or ADC staff. The purpose of this form is to record all prescription medications taken
by the subject within the two weeks before the current visit. For prescription medications not listed here, please follow the
instructions at the end of this form. OTC (non-prescription) medications need not be reported; however, a short list of medications
that could be either prescription or OTC follows the prescription list.
</span>
"""

INSTR_IVP_A5  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician or ADC staff.
For additional clarification and examples, see UDS Coding Guidebook for Initial Visit Packet, Form A5.
</span>
"""

INSTR_IVP_B1  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician.
For additional clarification and examples, see UDS Coding Guidebook for Initial Visit Packet, Form B1.
</span>
"""

INSTR_IVP_B4  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician or other trained health professional, based on co-participant report and neurological
exam of the subject. In the extremely rare instances when no co-participant is available, the clinician or other trained health
professional must complete this form using all other available information and his/her best clinical judgment. Score only as decline
from previous level due to cognitive loss, not impairment due to other factors, such as depression or PTSD.
For further information, see UDS Coding Guidebook for Initial Visit Packet, Form B4.
</span>
"""

INSTR_IVP_B5 = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician or other trained health professional based on co-participant interview, as described by the training video.
(This is not to be completed by the subject as a paper-and-pencil self-report.)
For information on NPI-Q Interviewer Certification, see UDS Coding Guidebook for Initial Visit Packet, Form B5.
</span>
"""

INSTR_IVP_B6 = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician or other trained health professional, based on subject response.
For additional clarification and examples, see UDS Coding Guidebook for Initial Visit Packet, Form B6.
</span>
"""

INSTR_IVP_B7 = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician or other trained health professional, based on information provided by the co-participant.
For further information, see UDS Coding Guidebook for Initial Visit Packet, Form B7.
</span>
"""

INSTR_IVP_B8 = """
<span style='font-weight: normal; font-style: italic;'>
This form must be completed by a clinician with experience in assessing the neurological signs listed below and in attributing the
observed findings to a particular syndrome. Please use your best clinical judgment in assigning the syndrome.
For additional clarification and examples, see UDS Coding Guidebook for Initial Visit Packet, Form B8.
</span>
"""

INSTR_IVP_B9 = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician.
For additional clarification and examples, see UDS Coding Guidebook for Initial Visit Packet, Form B9.
</span>
"""

INSTR_IVP_C2 = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by ADC or clinic staff.
For test administration and scoring, see Instructions for Neuropsychological Battery Form C2.
</span>

KEY: If the subject cannot complete any of the following exams, please give the reason by entering one of the following codes:
95 / 995 = Physical problem
96 / 996 = Cognitive/behavior problem
97 / 997 = Other problem
98 / 998 = Verbal refusal
"""

INSTR_IVP_D1 = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician.
For additional clarification and examples, see UDS Coding Guidebook for Initial Visit Packet, Form D1.
</span>
<h3>
This form is divided into three main sections:
Section 1 - Cognitive status: Normal cognition / MCI / dementia and clinical syndrome

Section 2 - Biomarkers, imaging, and genetics: Neurodegenerative imaging and CSF biomarkers, imaging evidence for CVD, and known genetic mutations for AD and FTLD

Section 3 - Etiological diagnoses: presumed etiological diagnoses for the cognitive disorder
</h3>
"""

INSTR_IVP_D2 = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by a physician, physician's assistant, nurse practitioner, or other qualified practitioner.
For additional clarifications and examples, see UDS Coding Guidebook for Initial Visit Packet, Form D2.
</span>
"""


# === FVP Instructions
INSTR_FVP_A1  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by intake interviewer based on ADC scheduling records, subject interview, medical records, and co-participant report (as needed). For additional clarification and examples, see UDS Coding Guidebook for Follow-up Visit Packet, Form A1.
</span>
To print a copy of data collected for this form at a previous UDS visit, go to https://www.alz.washington.edu/MEMBER/siteprint.html
"""

INSTR_FVP_A2  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by intake interviewer based on co-participant's report.
For additional clarification and examples, see UDS Coding Guidebook for Follow-up Visit Packet, Form A2.
</span>

To print a copy of data collected for this form at a previous UDS visit, go to https://www.alz.washington.edu/MEMBER/siteprint.html
"""


INSTR_FVP_A3  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by a clinician with experience in evaluating patients with neurological problems and psychiatric conditions.
For additional clarification and examples, see UDS Coding Guidebook for Follow-up Visit Packet, Form A3.
</span>

For subjects who are receiving UDS Version 3 of Form A3 for the first time:

<span style='font-weight: normal;'>
Please answer Yes to Question 1 and continue to provide all known information on all biological parents, siblings, and children, even if you
have provided similar information on a UDS Version 2 Form A3.
</span>

Corrections or new information on previously submitted family members -

<span style='font-weight: normal;'>
For family members who were denoted as being affected with a neurological or psychiatric condition or who were not affected at a previous UDS visit,
any corrections to their data should be made to that previous A3 Form. Any newly obtained information
 (e.g., new mutation information, new diagnoses, new method of evaluation), including for family members previously reported as being affected
at a past UDS visit, should be indicated on this form and should not be submitted as a correction to a previously submitted Form A3.

A summary of all previously submitted family history data can be found at: https://www.alz.washington.edu/MEMBER/siteprint.html.
</span>
"""


INSTR_FVP_A4  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician or ADC staff.
The purpose of this form is to record all prescription medications taken by the subject <b>within the two weeks before the current visit</b>.
For prescription medications not listed here, please follow the instructions at the end of this form.
OTC (non-prescription) medications need not be reported; however, a short list of medications that could be either prescription or OTC follows the prescription list.
</span>
"""

INSTR_FVP_B1  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician.
For additional clarification and examples, see UDS Coding Guidebook for Follow-up Visit Packet, Form B1.
</span>
"""

INSTR_FVP_B4  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician or other trained health professional, based on co-participant report and neurological exam of the subject.
In the extremely rare instances when no co-participant is available, the clinician or other trained health professional must complete this form
using all other available information and his/her best clinical judgment. Score only as decline from previous level due to cognitive loss, not
impairment due to other factors, such as depression or PTSD.
For further information, see UDS Coding Guidebook for Follow-up Visit Packet, Form B4.
</span>
"""

INSTR_FVP_B5  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician or other trained health professional based on co-participant interview, as described by the training video.
(This is not to be completed by the subject as a paper-and-pencil self-report.)
For information on NPI-Q Interviewer Certification, see UDS Coding Guidebook for Follow-up Visit Packet, Form B5.
</span>
"""

INSTR_FVP_B6  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician or other trained health professional, based on subject response.
For additional clarification and examples, see UDS Coding Guidebook for Follow-up Visit Packet, Form B6.
</span>
"""

INSTR_FVP_B7  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician or other trained health professional, based on information provided by the co-participant.
For further information, see UDS Coding Guidebook for Follow-up Visit Packet, Form B7.
Indicate the level of performance for each activity by selecting the appropriate response.
</span>
"""

INSTR_FVP_B8  = """
<span style='font-weight: normal; font-style: italic;'>
This form must be completed by a clinician with experience in assessing the neurological signs listed below and
in attributing the observed findings to a particular syndrome. Please use your best clinical judgment in assigning the syndrome.
For additional clarification and examples, see UDS Coding Guidebook for Follow-up Visit Packet, Form B8.
</span>
"""

INSTR_FVP_B9  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician.
For additional clarification and examples, see UDS Coding Guidebook for Follow-up Visit Packet, Form B9.
</span>
"""

INSTR_FVP_C1  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by ADC or clinic staff.
For test administration and scoring, see Instructions for Neuropsychological Battery Form C1.
</span>

PROTOCOL FOR ADMINISTERING the neuropsychological battery for UDS Version 3 FVP (using either Form C1 or Form C2):
<b>
For subjects who had already been seen for one or more UDS visits before the implementation of Version 3, you may:
</b>
    a) continue to follow those subjects with the old neuropsychological battery (Form C1);
    - OR -
    b) switch those subjects to the new neuropsychological battery (Form C2).
    A given subject may be switched to the new battery at any time after Version 3 implementation, at the Center's discretion.
"""

INSTR_FVP_C2  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by ADC or clinic staff. For test administration and scoring, see Instructions for Neuropsychological Battery Form C2.
</span>
"""

INSTR_FVP_D1  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by the clinician.
For additional clarification and examples, see UDS Coding Guidebook for Follow-up Visit Packet, Form D1.
</span>
<h3>
This form is divided into three main sections:
Section 1 - Cognitive status: Normal cognition / MCI / dementia and clinical syndrome

Section 2 - Biomarkers, imaging, and genetics: Neurodegenerative imaging and CSF biomarkers, imaging evidence for CVD, and known genetic mutations for AD and FTLD

Section 3 - Etiological diagnoses: presumed etiological diagnoses for the cognitive disorder
</h3>
"""

INSTR_FVP_D2  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by a physician, physician's assistant, nurse practitioner, or other qualified practitioner.
For additional clarifications and examples, see UDS Coding Guidebook for Follow-up Visit Packet, Form D2.
</span>
"""

INSTR_FVP_Z1  = """
<span style='font-weight: normal; font-style: italic;'>
This form is to be completed by clinic staff.
</span>
NACC expects and intends that all UDS forms will be attempted on all subjects, but we realize this may be impossible when
the patient is terminally ill, or when there is no co-participant, or for other reasons. However, for a subject to be
included in the UDS database, Forms Z1, A1, B4, B8, B9, C1/C2, D1, and D2 must be submitted, even though these forms may include some items with missing data. An explanation is required below for forms that are not submitted.

KEY: If the specified form was not completed, please enter one of the following codes:
95 = Physical problem
96 = Cognitive or behavioral problem
97 = Other problem 98=Verbal refusal

Center IDs:
2 = Boston University
3 = Case Western University 4 = Columbia University
5 = Duke University
6 = Emory University
7 = Massachusetts ADRC
8 = Indiana University
9 = Johns Hopkins University
10 = Mayo Clinic
11 = Mount Sinai
12 = New York University
13 = Northwestern University
14 = Oregon Health & Science University 15 = Rush University
16 = University of California, Davis
17 = University of California, Los Angeles 18 = University of California, San Diego
19 = University of Kentucky
20 = University of Michigan
21 = University of Pennsylvania
22 = University of Pittsburgh
25 = University of Texas Southwestern
26 = University of Washington
27 = Washington University in Saint Louis 28 = University of Alabama
30 = University of Southern California
31 = University of California, Irvine
32 = Stanford University
33 = Arizona ADC
34 = University of Arkansas
35 = University of California, San Francisco 36 = Florida ADC
37 = University of Wisconsin
38 = University of Kansas
"""

#'z11': {'file': '?.csv',  'name': 'z1_form_checklist',},
naming = {

    'ivp_extra': {
        'title': 'INITIAL VISIT PACKET',
    },
    'fvp_extra': {
        'title': 'FOLLOW-UP VISIT PACKET',
    },
    'ivp': {
        'z1': {'file': 'uds3dedZ1IVP.csv',  'name': 'z1_form_checklist',
            'descr': 'Form Checklist',
            'instr': INSTR_IVP_Z1 },
        'a1': {'file': 'uds3dedA1IVP.csv',  'name': 'a1_subject_demographics',
            'descr': 'Subject Demographics',
            'instr': INSTR_IVP_A1 },
        'a2': {'file': 'uds3dedA2IVP.csv',  'name': 'a2_co_participant_demographics',
            'descr': 'Co-Participant Demographics',
            'instr': INSTR_IVP_A2 },
        'a3': {'file': 'uds3dedA3IVP.csv',  'name': 'a3_subject_family_history',
            'descr': 'Subject Family History',
            'instr': INSTR_IVP_A3},
        'a4': {'file': 'uds3dedA4DIVP.csv', 'name': 'a4_subject_medications',
            'descr': 'Subject Medications',
            'instr': INSTR_IVP_A4},
        'a5': {'file': 'uds3dedA5IVP.csv',  'name': 'a5_subject_health_history',
            'descr': 'Subject Health History',
            'instr': INSTR_IVP_A5 },
        'b1': {'file': 'uds3dedB1IVP.csv',  'name': 'b1_evaluation_form_physical',
            'descr': 'Evaluation Form Physical',
            'instr': INSTR_IVP_B1 },
        'b4': {'file': 'uds3dedB4IVP.csv',  'name': 'b4_global_staging_cdr_standard_and_supplemental',
            'descr': 'Global Staging CDR Standard and Supplemental',
            'instr': INSTR_IVP_B4 },
        'b5': {'file': 'uds3dedB5IVP.csv',  'name': 'b5_behavioral_assessment_npiq',
            'descr': 'Behavioral Assessment NPI-Q',
            'instr': INSTR_IVP_B5},
        'b6': {'file': 'uds3dedB6IVP.csv',  'name': 'b6_behavioral_assessment_gds',
            'descr': 'Behavioral Assessment GDS',
            'instr': INSTR_IVP_B6},
        'b7': {'file': 'uds3dedB7IVP.csv',  'name': 'b7_functional_assessment_faq',
            'descr': 'Functional Assessment FAQ',
            'instr': INSTR_IVP_B7},
        'b8': {'file': 'uds3dedB8IVP.csv',  'name': 'b8_evaluation_neurological_exam_findings',
            'descr': 'Evaluation - Neurological Exam Findings',
            'instr': INSTR_IVP_B8},
        'b9': {'file': 'uds3dedB9IVP.csv',  'name': 'b9_clinician_judgment_of_symptoms',
            'descr': 'Clinician Judgment of Symptoms',
            'instr': INSTR_IVP_B9},
        'c2': {'file': 'uds3dedC2IVP.csv',  'name': 'c2_neuropsychological_battery_scores',
            'descr': 'Neuropsychological Battery Scores',
            'instr': INSTR_IVP_C2},
        'd1': {'file': 'uds3dedD1IVP.csv',  'name': 'd1_clinician_diagnosis',
            'descr': 'Clinician Diagnosis',
            'instr': INSTR_IVP_D1},
        'd2': {'file': 'uds3dedD2IVP.csv',  'name': 'd2_clinician_assessed_medical_conditions',
            'descr': 'Clinician-assessed Medical Conditions',
            'instr': INSTR_IVP_D2},
    },
    'fvp': {
        'z1': {'file': 'uds3dedZ1FVP.csv',  'name': 'z1_form_checklist',
            'descr': 'Form Checklist',
            'instr': INSTR_FVP_Z1 },
        'a1': {'file': 'uds3dedA1FVP.csv',  'name': 'a1_subject_demographics',
            'descr': 'Subject Demographics',
            'instr': INSTR_FVP_A1 },
        'a2': {'file': 'uds3dedA2FVP.csv',  'name': 'a2_co_participant_demographics',
            'descr': 'Co-Participant Demographics',
            'instr': INSTR_FVP_A2 },
        'a3': {'file': 'uds3dedA3FVP.csv',  'name': 'a3_subject_family_history',
            'descr': 'Subject Family History',
            'instr': INSTR_FVP_A3 },
        'a4': {'file': 'uds3dedA4DFVP.csv', 'name': 'a4_subject_medications',
            'descr': 'Subject Medications',
            'instr': INSTR_FVP_A4 },
        'b1': {'file': 'uds3dedB1FVP.csv',  'name': 'b1_evaluation_form_physical',
            'descr': 'Evaluation Form Physical',
            'instr': INSTR_FVP_B1 },
        'b4': {'file': 'uds3dedB4FVP.csv',  'name': 'b4_global_staging_cdr_standard_and_supplemental',
            'descr': 'Global Staging CDR Standard and Supplemental',
            'instr': INSTR_FVP_B4 },
        'b5': {'file': 'uds3dedB5FVP.csv',  'name': 'b5_behavioral_assessment_npiq',
            'descr': 'Behavioral Assessment NPI-Q',
            'instr': INSTR_FVP_B5 },
        'b6': {'file': 'uds3dedB6FVP.csv',  'name': 'b6_behavioral_assessment_gds',
            'descr': 'Behavioral Assessment GDS',
            'instr': INSTR_FVP_B6 },
        'b7': {'file': 'uds3dedB7FVP.csv',  'name': 'b7_functional_assessment_faq',
            'descr': 'Functional Assessment FAQ',
            'instr': INSTR_FVP_B7 },
        'b8': {'file': 'uds3dedB8FVP.csv',  'name': 'b8_evaluation_neurological_exam_findings',
            'descr': 'Evaluation - Neurological Exam Findings',
            'instr': INSTR_FVP_B8 },
        'b9': {'file': 'uds3dedB9FVP.csv',  'name': 'b9_clinician_judgment_of_symptoms',
            'descr': 'Clinician Judgment of Symptoms',
            'instr': INSTR_FVP_B9 },
        'c1': {'file': 'uds3dedC1FVP.csv',  'name': 'c1_neuropsychological_battery_scores',
            'descr': 'Neuropsychological Battery Scores',
            'instr': INSTR_FVP_C1 },
        'c2': {'file': 'uds3dedC2FVP.csv',  'name': 'c2_neuropsychological_battery_scores',
            'descr': 'Neuropsychological Battery Scores',
            'instr': INSTR_FVP_C2 },
        'd1': {'file': 'uds3dedD1FVP.csv',  'name': 'd1_clinician_diagnosis',
            'descr': 'Clinician Diagnosis',
            'instr': INSTR_FVP_D1 },
        'd2': {'file': 'uds3dedD2FVP.csv',  'name': 'd2_clinician_assessed_medical_conditions',
            'descr': 'Clinician-assessed Medical Conditions',
            'instr': INSTR_FVP_D2 },
    },
}


