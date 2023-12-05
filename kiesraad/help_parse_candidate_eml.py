#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 18:00:21 2023

@author: baswork
"""

import xml.etree.ElementTree as ET

def parse_candidate_eml(file_name):
    
    tree = ET.parse(file_name)
    root = tree.getroot()
    
    out = list()
    
    namespace = {
    'eml': 'urn:oasis:names:tc:evs:schema:eml',
    'kr': 'http://www.kiesraad.nl/extensions',
    'xnl': 'urn:oasis:names:tc:ciq:xsdschema:xNL:2.0',
    'xal': 'urn:oasis:names:tc:ciq:xsdschema:xAL:2.0'
}
    # Extracting specific elements
    issue_date = root.find('.//eml:IssueDate', namespace).text
    election_name = root.find('.//eml:ElectionName', namespace).text

    # Extracting candidate information
    candidates = root.findall('.//eml:Candidate', namespace)
    affiliations = root.findall('.//eml:Affiliation', namespace)
    for affiliation in affiliations:
        # Within each 'Affiliation', find 'Candidate' elements
        candidates = affiliation.findall('.//eml:Candidate', namespace)
        for candidate in candidates:
            # Find 'RegisteredName' within the 'Affiliation'
            registered_name = affiliation.find('.//eml:RegisteredName', namespace)
            # Extract 'RegisteredName' if found, otherwise set it as "N/A"
            registered_name_text = registered_name.text if registered_name is not None else "NA"
            # Find party ID
            affiliation_id = affiliation.find('.//eml:AffiliationIdentifier', namespace)
            if affiliation_id is not None:
                party_id = affiliation_id.get('Id')
            else:
                party_id = "NA"
            
            candidate_id = candidate.find('.//eml:CandidateIdentifier', namespace).attrib['Id']
            name_elements = candidate.find('.//xnl:PersonName', namespace)
            
            if name_elements.find('.//xnl:FirstName', namespace) is not None:
                first_name = name_elements.find('.//xnl:FirstName', namespace).text
            else:
                first_name = "NA"
                
            if name_elements.find(".//xnl:NameLine", namespace) is not None:
                voorletters = name_elements.find(".//xnl:NameLine", namespace).text
            else:
                voorletters = "NA"
            
            if name_elements.find(".//xnl:NamePrefix", namespace) is not None:
                  prefix = name_elements.find(".//xnl:NamePrefix", namespace).text
            else:
                  prefix = ""
            
            if name_elements.find('.//xnl:LastName', namespace).text is not None:
                last_name =  name_elements.find('.//xnl:LastName', namespace).text
            else:
                last_name = "NA"
            
            gender_element = candidate.find('.//eml:Gender', namespace)
            if gender_element is not None and gender_element.text is not None:
                gender = gender_element.text
            else:
                gender = "NA"
            
            qualifying_address = candidate.find('.//eml:QualifyingAddress', namespace)
            if qualifying_address is not None:
                locality_name = qualifying_address.find('.//xal:LocalityName', namespace).text
            else:
                locality_name = "NA"
            
            out.append({'candidate_id': candidate_id, 
                        'party_name' : registered_name_text,
                        'party_id': party_id,
                       'firstname': first_name, 
                       'initials': voorletters,
                       'prefix': prefix,
                       'lastname': last_name,
                       'gender': gender, 
                       'locality_name': locality_name})
            
    return out
        
        
#test = parse_candidate_eml('../data/tk2021/Kandidatenlijsten_TK2021_Amsterdam.eml.xml')
#test
#pd.DataFrame(test)