#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 16:44:57 2023

@author: baswork

Function; find_relevant_candidate_list_for_csv file

Step 1: Finds the candidate lists for each per-candidate csv file
Step 2: Merges the candidate info into the per-candidate csv file
Step 3: Aggregates the per-candidate csv file to the municipal level 
(Rather than the voting bureau-level)
"""

import os
from pathlib import Path
import pandas as pd
import parse_eml
from help_parse_candidate_eml import parse_candidate_eml

# List all files in the directory
directory = '../data/tk2021'
files = os.listdir(directory)
kandidaten_lijsten = [i for i in files if 'Kandidatenlijsten' in i]

def find_relevant_candidate_list_for_csv_file(csv_file):
    
    data = pd.read_csv(csv_file)
    kieskring_name = pd.unique(data['contest_name'])[0]
    
    candidate_list_file = (next((filename for filename 
                                 in kandidaten_lijsten 
                                 if kieskring_name in filename), None)
                           )
    
    url = '../data/tk2021/' + candidate_list_file
    candidate_df = pd.DataFrame(parse_candidate_eml(url))
    
    # Modify the data.frame identifiers to integers 
    candidate_df['party_id'] = candidate_df['party_id'].astype('int64')
    candidate_df['candidate_id'] = candidate_df['candidate_id'].astype('int64')
    data['party_id'] = data['party_id'].astype('int64')
    data['candidate_identifier'] = data['candidate_identifier'].astype('int64')
    
    # Merge
    data_with_candidate_info = pd.merge(
        data, candidate_df,
        how='left',
        left_on=['party_id', 'candidate_identifier'], 
        right_on=['party_id', 'candidate_id']
        )
    
    # Group by - aggregate to the municipal level
    


data = pd.read_csv('../data/tk2021/csv/Telling_TK2021_gemeente_Aa_en_Hunze.eml_per_candidate.csv')
kieskring_name = pd.unique(data['contest_name'])[0]

candidate_list_file = (next((filename for filename 
                             in kandidaten_lijsten 
                             if kieskring_name in filename), None)
                       )

url = '../data/tk2021/' + candidate_list_file
candidate_df = pd.DataFrame(parse_candidate_eml(url))
candidate_df['party_id'] = candidate_df['party_id'].astype('int64')
candidate_df['candidate_id'] = candidate_df['candidate_id'].astype('int64')
data['party_id'] = data['party_id'].astype('int64')
data['candidate_identifier'] = data['candidate_identifier'].astype('int64')

data_with_candidate_info = pd.merge(
    data, candidate_df,
    how='left',
    left_on=['party_id', 'candidate_identifier'], 
    right_on=['party_id', 'candidate_id']
    )

data_with_candidate_info