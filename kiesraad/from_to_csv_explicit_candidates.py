#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 16:44:57 2023

@author: baswork
"""

import os
from pathlib import Path
import pandas as pd
import parse_eml

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


data = pd.read_csv('../data/tk2021/csv/Telling_TK2021_gemeente_Aa_en_Hunze.eml_per_candidate.csv')
kieskring_name = pd.unique(data['contest_name'])[0]

candidate_list_file = (next((filename for filename 
                             in kandidaten_lijsten 
                             if kieskring_name in filename), None)
                       )

test = parse_eml.parse_eml(candidate_list_file)

parse_eml.create_candidate_list(Path('../data/tk2021'))