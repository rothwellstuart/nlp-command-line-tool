
# coding: utf-8

# # Catalogue_classification_v1_0
#
# Create a high level classification of files by file type
#
# Output file list:
# - filename
# - file hash
# - classification type
#
# Output summary:
# - classification type
# - number of files
# - total size in bytes
#
# V1.3: added mimetype of application with extension of ".MSG" to assign fileclass of EMAIL



# Imports

import os, sys, magic, time, hashlib, csv, shutil
from os import listdir, environ
from os.path import isfile, join

import pandas as pd



# Initialise variables
allfiles=[]
urn = 0


# Main loop
for subdir, dirs, files in os.walk(selected_dir):
    for file in files:
        urn += 1
        filesize = os.path.getsize(join(subdir, file))
        fileext = os.path.splitext(join(subdir, file))[1].upper()
        mimetype = magic.from_file(join(subdir, file), mime=True)

        row=[]
        row.append(urn)
        row.append(file)
        row.append(hashlib.sha1(file.encode()).hexdigest())
        row.append(filesize)
        row.append(mimetype)
        row.append(fileext)


        # CLASSIFICATION
        if 'encrypted' in mimetype:
            fileclass = 'ENCRYPTED'
        elif 'zip' in mimetype:
            fileclass = 'COMPRESSED'
        elif 'word' in mimetype:
            fileclass = 'WORD'
        elif 'pdf' in mimetype:
            fileclass='PDF'
        elif ('excel' in mimetype) or ('spreadsheet' in mimetype):
            fileclass = 'EXCEL'
        elif 'office' in mimetype and fileext == '.VSD':
            fileclass = 'VISIO'
        elif 'office' in mimetype and fileext == '.XLS':
            fileclass = 'EXCEL'
        elif 'powerpoint' in mimetype:
            fileclass = 'POWERPOINT'
        elif 'image' in mimetype:
            fileclass = 'IMAGE'
        elif 'message' in mimetype:
            fileclass = 'EMAIL'
        elif 'text' in mimetype or 'octet-stream' in mimetype or 'application' in mimetype:
            if fileext == '.HTM' or fileext == '.HTML':
                fileclass = 'HTML'
            elif fileext == '.EML' or fileext == '.RTF' or fileext == '.MSG':
                fileclass = 'EMAIL'
            elif fileext == '.TXT':
                fileclass = 'TEXT'
            elif fileext == '.RAW' or fileext == '.GIF' or fileext == '.JPG' or fileext == '.PNG' or '.TIF' in fileext or fileext == '.WMF':
                fileclass = 'IMAGE'
            elif fileext == '.DAT' or fileext == '.CSV':
                fileclass = 'FLATFILE'
            elif '.DOC' in fileext:
                fileclass = 'WORD'
            elif fileext == '.PDF':
                fileclass = 'PDF'
            elif '.XLS' in fileext:
                fileclass = 'EXCEL'
            elif '.PPT' in fileext:
                fileclass = 'POWERPOINT'
            elif fileext == '.MBOX':
                fileclass = 'MAILBOX'
            elif fileext == '.XML':
                fileclass = 'XML'
            elif fileext == '.ZIP':
                fileclass = 'COMPRESSED'
            elif '.001' in fileext or fileext == '.JS' or fileext == '.AU_' or fileext == '.COM_' or fileext == '.CSS' or \
                    fileext == '.JOBOPTIONS' or fileext == '.LOCAL_' or fileext == '.DOT' or fileext == '.DS_STORE' or \
                    fileext == '.EMF' or fileext == '.MDB' or fileext == '.ODTTF' or fileext == '.PART' or fileext == '.WPD':
                fileclass = 'MISC'
            else:
                fileclass = 'MISC'
        elif mimetype == 'application/xml':
            fileclass = 'XML'
        else:
            ### octet-stream
            ### inode/x-empty
            fileclass='UNKNOWN'

        row.append(fileclass)

        allfiles.append(row)

### End of main loop through files



# Convert to DataFrame
allfiles_df = pd.DataFrame(allfiles)

# Rename columns
allfiles_df.columns = ['seq_no', 'filepath', 'filehash', 'size', 'mimetype', 'fileext', 'fileclass']

# Split out mimetype
# allfiles_df[['mime1', 'mime2']] = pd.DataFrame(allfiles_df.mimetype.str.split('/').tolist(), columns=['mime1', 'mime2'])

# print(allfiles_df.head(30))


### Summarise by file type

# File count
summary_count = allfiles_df[['filepath', 'fileclass']].groupby(['fileclass']).count()
filecount_total = summary_count.sum()
summary_count['percent'] = round(100* summary_count['filepath'] / float(filecount_total), 1)
summary_count.rename(columns={'filepath': 'num_files', 'percent': 'perc_num_files'}, inplace=True)


# File size
summary_size = allfiles_df[['size', 'fileclass']].groupby(['fileclass']).sum()
size_total = summary_size.sum()
summary_size['percent'] = round(100 * summary_size['size'] / float(size_total), 1)
summary_size.rename(columns={'percent': 'perc_size'}, inplace=True)

# Merge together num_files and size
summary_fileclass = pd.merge(summary_count, summary_size, left_index=True, right_index=True)
summary_fileclass

print("Summary by file class:\n", summary_fileclass)



# Summarise by fileclass, mimetype AND file extension, to QA correct assignment of fileclass
summary_count_crossed = allfiles_df[['filepath', 'fileclass', 'mimetype', 'fileext']].groupby(['fileclass', 'mimetype', 'fileext']).count()
filecount_total_crossed = summary_count_crossed.sum()
summary_count_crossed['perc_num_files'] = round(100 * summary_count_crossed['filepath'] / float(filecount_total_crossed), 1)
summary_count_crossed.rename(columns={'filepath': 'num_files'}, inplace=True)

# File size
summary_size_crossed = allfiles_df[['size', 'fileclass', 'mimetype', 'fileext']].groupby(['fileclass', 'mimetype', 'fileext']).sum()
size_total_crossed = summary_size_crossed.sum()
summary_size_crossed['perc_size'] = round(100 * summary_size_crossed['size'] / float(size_total_crossed), 1)

# Merge num_files and size summaries together
summary_crossed = pd.merge(summary_count_crossed, summary_size_crossed, left_index=True, right_index=True)



# Export files
# Output to csv
allfiles_df.to_csv('output/01_catalogue_fileclass_file_level.csv', index=False)


# Output summary stats to file
summary_fileclass.to_csv('output/01_catalogue_fileclass_summary.csv', index=False)


# Output QA summary stats to file
summary_crossed.reset_index().to_csv('output/01_catalogue_fileclass_qa.csv')


print("\nSee output/01_catalogue_fileclass_level.csv for list of files tagged with their assigned fileclass.")
print("See output/01_catalogue_fileclass_summary.csv for the distribution of file count and file size by fileclass.")
print("See output/01_catalogue_fileclass_qa.csv for the full breakdown of fileclass by file extension - this can be used to adjust file classificatyin rules.")
print("\n\n\n")
