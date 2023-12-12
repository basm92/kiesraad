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
import re
import parse_eml
from help_parse_candidate_eml import parse_candidate_eml

# List all files in the directory


def find_relevant_candidate_list_for_csv_file(csv_file, candidate_list_directory):
    # First identify the candidate lists
    files = os.listdir(candidate_list_directory)
    kandidaten_lijsten = [i for i in files if 'Kandidatenlijsten' in i]
    
    # Identify the .csv file with the votes per candidates per bureau
    data = pd.read_csv(csv_file)
    kieskring_name = pd.unique(data['contest_name'])[0]
    modified_kieskring_name = re.compile(r"^'s-").sub('', kieskring_name)
    modified_kieskring_name = re.sub(r'^Den\s', '', modified_kieskring_name) 
    
    candidate_list_file = (next((filename for filename 
                                 in kandidaten_lijsten 
                                 if modified_kieskring_name in filename), None)
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
    
    data_with_candidate_info.drop(columns=['party_name_x'], inplace=True)
    
    #columns_to_group_by = 
    excluded_columns = ['postcode', 'station_name', 'station_id', 'election_domain_name', 'election_domain_id', 'votes'] # Select the columns you want to exclude by index
    included_columns = [col for col in data_with_candidate_info.columns if col not in excluded_columns]

    result = data_with_candidate_info.groupby(included_columns)['votes'].sum().reset_index()
    output_name = csv_file[:-4] + '_' + 'corrected.csv'
    result.to_csv(output_name)


for i in os.listdir('../data/tk2021/csv/'):
    if 'per_candidate.csv' in i:
        file = '../data/tk2021/csv/' + i
        find_relevant_candidate_list_for_csv_file(file, '../data/tk2021')

