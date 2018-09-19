
### ENTITY_EXTRACTION_SPACY_V3_0.PY


import os, re, email, csv, json, fnmatch, csv
from collections import Counter
from os.path import isfile, join
import pandas as pd
# import arrow

# Import spacy and English models
import spacy, numpy, magic

# Load English Spacy module
nlp = spacy.load('en')

print("DEBUG: GOT TO HERE")

# Initialise variables
driverfile = 'output/01_catalogue_fileclass_file_level.csv'
subdir = selected_dir

# Read in driver file
driver_df = pd.read_csv(driverfile)

# Keep only qualifying rows
driver_pass = driver_df.loc[driver_df['fileclass'] in ['EMAIL', 'TEXT', 'FLATFILE']]
#
# # Convert PASSes to list
# driver_list = driver_pass['filepath'].tolist()
#
# print("DEBUG: DRIVER_LIST = ", driver_list)
#
# ### Main Loop
# for file in driver_list:
#
#     counter += 1
#     entities=[]
#
#     filename = join(subdir, file)
#     sample = open(filename, 'r', encoding='utf-8', errors='ignore').read()
#     print("Processing file ", counter, ": ", filename)
#
#     # Run entity extraction on email body
#     try:
#         nlpd = nlp(sample)
#         # Ony retain entities of types we are interested in
#         nlpd.ents = [ent for ent in nlpd.ents if ent.label_ in ('PERSON', 'FACILITY', 'ORG', 'GPE', 'LOC', 'PRODUCT')]
#
#         # Loop on Entitites Extracted
#         for ent in nlpd.ents:
#             ent_entry = [re.sub('\s+',' ',str(ent).rstrip()), ent.label_]
#             entities.append([filename, ent, ent.label_])
#
#     except:
#         print('Could not NLP the file')
#         files_not_processed.append([filename, 'NLP error'])
#
# # Output to CSVs
# if entities:
#     with open('output/02_extracted_entities_nlp.csv', 'w', newline="") as outfile2:
#         writer = csv.writer(outfile2)
#         writer.writerow(['filename', 'entity', 'entity_type'])
#         writer.writerows(entities)
#
#
#
# if files_not_processed:
#     with open('output/02_entity_extraction_nlp_skipped_files.csv', 'w', newline="") as outfile3:
#         writer = csv.writer(outfile3)
#         writer.writerow(['filename', 'reason'])
#         writer.writerows(files_not_processed)
#
# print("Finished running NLP entity extraction.")
# print("Found ", len(entities), " instances of entities.")
# print("See output/02_extracted entities_nlp.csv for details of the entities found.")
# print("See output/02_extracted entities_nlp_skipped_files.csv for details of files that could not be processed.")
