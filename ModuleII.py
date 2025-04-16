# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 18:09:50 2025

@author: Lauris
"""

from chembl_webresource_client.new_client import new_client 
import requests, sys

molecule = new_client.molecule

'''
#############################################################
Exercise 1
#############################################################
'''
# Get all approved drugs ordered by approval date and name
drugs_ordered = molecule.filter(max_phase=4).order_by('first_approval', 'pref_name')

# Get only the approval date and name in order for visibility purposes
drugs_ordered_only = molecule.filter(max_phase=4).only('first_approval', 'pref_name').order_by('first_approval', 'pref_name')

#print(drugs_ordered_only)

'''
#############################################################
Exercise 2
#############################################################
'''

uniprots_accession_numbers = []

# Retrieves all drugs approved after 2019 
# You can fetch as many fields as you want from this query but the molecule_chembl_id is needed
drugs_2019 = molecule.filter(first_approval__gte=2019).only('molecule_chembl_id', 'pref_name').order_by('first_approval')

#print(drugs_2019)

mechanism = new_client.mechanism
molecule_target = []

'----------------------------------------'

# This will look in the mechanism table for the molecule_chembl_id
# and get all target_chembl_id's associated with the given molecule and return them as a list
def find_target_ids(molecule_id):
    
    # Retrieve all target ids associated with a given molecule id
    # Type: List of dictionaries with Key: target_chembl_id
    target_ids = mechanism.filter(molecule_chembl_id=molecule_id).only('target_chembl_id')
    
    id_list = [] # Create a list to store the target ids in
    
    # Only consider non empty lists since not every molecule is in the mechanism table
    if len(target_ids) == 0 or target_ids is None:
        return []

    
    # Iterate through each target id in the target_ids List to only get the id 
    for target_id in target_ids:
        if target_id['target_chembl_id'] is None: # Check if a given molecule has no target id associated to it
            continue
        
        id_list.append(target_id['target_chembl_id']) # Add each individual id to a list
        
    return id_list

'--------------------------------------'

# Iterate through all drugs and add the target ids to the dictionary
for drug in drugs_2019:
    targets = find_target_ids(drug['molecule_chembl_id'])
    
    drug.update({'target_chembl_ids': targets}) # Add the list with all ids to the molecule dictionary
    molecule_target.append(drug) # Add the updated molecule dictionary to a new list
        
#print(molecule_target[7])
       
target = new_client.target

'-------------------------------------'

# find all accession numbers associated to a target Id 
# input: target_id (can be a list or single string value)
# output: list of accession numbers (strings)
def find_accession_numbers(target_ids):
    
    # turn strings into a list of strings
    if not isinstance(target_ids, list):
        target_ids = [target_ids]
        
    # if the input is None or an empty list return an empty list    
    if target_ids is None or len(target_ids) <= 0:
        return []
    
    accession_numbers = []
    
    for target_id in target_ids:
        
        # each components is a list of dictionaries holding the accession numbers
        components = target.get(target_id)['target_components']
        
        if components is None or len(components) == 0: # Check for empty Lists/Objects and skip the iteration if thats the case
            continue
        
        for component in components:
            accession_number = component['accession'] # Fetches only the accession number for each entry in the components list
            
            # Skip the current iteration if a given target is not a protein or the number is already in the list
            if component['component_type'] != "PROTEIN" or accession_number in accession_numbers: 
                continue
            
            accession_numbers.append(accession_number) # add the accession numbers to a temporary list
    
    return accession_numbers
    
'------------------------------------'

molecule_accession = molecule_target

# loop through each molecule and find their accession numbers and add them to the dictionary 
for molecule in molecule_accession:
    accession_numbers = find_accession_numbers(molecule['target_chembl_ids'])
    molecule.update({'accession_numbers': accession_numbers})
    
    
#print(molecule_accession[2])


'''
#################################################################
Exercise 3
#################################################################
'''

molecule_keywords = molecule_accession
# Remove all drugs with no associated accession number
for drug in molecule_keywords:
    if len(drug['accession_numbers']) == 0 or drug['accession_numbers'] is None:
        molecule_keywords.remove(drug)

'-------------------------------------------'    

# get all keywords associated with a accession number or a list of accession numbers
# return: a list of all keywords
def fetch_keywords_ebi(accession_numbers):
    
    # turn strings into a list of strings
    if not isinstance(accession_numbers, list):
        accession_numbers = [accession_numbers]
        
    keyword_list = []
    for accession_number in accession_numbers:
        url = f"https://www.ebi.ac.uk/proteins/api/proteins/{accession_number}"
        r = requests.get(url, headers={ "Accept" : "application/json"})

        if not r.ok:
          r.raise_for_status()
          sys.exit()
        
        responseBody = r.json()
        keywords = responseBody.get('keywords', [])
        
        for keyword in keywords:
            keyword_list.append(keyword['value'])
    
    return keyword_list

'--------------------------------------------'

for drug in molecule_keywords:
    keywords = fetch_keywords_ebi(drug['accession_numbers'])
    drug.update({'keywords': keywords})

print(molecule_keywords[1])

    





