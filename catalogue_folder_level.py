# # Catalogue_folder_level
#
# Create a high level classification of files by file type, WITHIN A FOLDER
#

# Imports

# def catalogue_folder_level(selected_dir):

import os, sys, magic, time, hashlib, csv, shutil, operator
from os import listdir, environ
from os.path import isfile, join

import pandas as pd



# Initialise variables
allfiles=[]


# Main loop
# for file in driver_list:
for subdir, dirs, files in os.walk(selected_dir):

    dict_filecount=dict()
    dict_filesizes=dict()
    dict_mimecount=dict()
    dict_mimesizes=dict()
    dict_extcount=dict()
    dict_extsizes=dict()

    dict_filecount_sorted = []
    dict_filesizes_sorted = []
    dict_mimecount_sorted = []
    dict_mimesizes_sorted = []
    dict_extcount_sorted = []
    dict_extsizes_sorted = []

    folder_count = 0
    folder_size = 0

    # Get name of folder immediately above the files
    named_folder = subdir.rsplit('/',1)[-1]
    relpath = os.path.relpath(subdir, selected_dir)
    if relpath == '.':
        relpath = ""
    print("Processing sub-folder: ", named_folder, ", at: ", relpath)

    # Cycle through files
    for file in files:

        # Count of files
        folder_count += 1

        # Get filetype and file size
        filesize = os.path.getsize(join(subdir, file))
        fileext = os.path.splitext(join(subdir, file))[1].upper()
        mimetype = magic.from_file(join(subdir, file), mime=True)

        # Add in size
        folder_size += filesize

        # CLASSIFICATION of files
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

        # Add to dictionaries
        if fileclass in dict_filecount:
            dict_filecount[fileclass] += 1
            dict_filesizes[fileclass] += filesize
        else:
            dict_filecount[fileclass] = 1
            dict_filesizes[fileclass] = filesize

        if mimetype in dict_mimecount:
            dict_mimecount[mimetype] += 1
            dict_mimesizes[mimetype] += filesize
        else:
            dict_mimecount[mimetype] = 1
            dict_mimesizes[mimetype] = filesize

        if fileext in dict_extcount:
            dict_extcount[fileext] += 1
            dict_extsizes[fileext] += filesize
        else:
            dict_extcount[fileext] = 1
            dict_extsizes[fileext] = filesize

###### End loop of files within subdir

    # Sort dictionaries by the values
    dict_filecount_sorted = sorted(dict_filecount.items(), key=operator.itemgetter(1), reverse=True)
    dict_filesizes_sorted = sorted(dict_filesizes.items(), key=operator.itemgetter(1), reverse=True)
    dict_mimecount_sorted = sorted(dict_mimecount.items(), key=operator.itemgetter(1), reverse=True)
    dict_mimesizes_sorted = sorted(dict_mimesizes.items(), key=operator.itemgetter(1), reverse=True)
    dict_extcount_sorted = sorted(dict_extcount.items(), key=operator.itemgetter(1), reverse=True)
    dict_extsizes_sorted = sorted(dict_extsizes.items(), key=operator.itemgetter(1), reverse=True)

    # Check contents of dictionaries
#    print('Filecounts by filetype: ', dict_filecount_sorted)
#    print('Filesizes by filetype', dict_filesizes_sorted)
#    print('Filecounts by mimetype: ', dict_mimecount_sorted)
#    print('Filesizes by mimetype', dict_mimesizes_sorted)
#    print('Filecounts by extension: ', dict_extcount_sorted)
#    print('Filesizes by extension', dict_extsizes_sorted)

    # Append to output - one row for every subdir
    row=[]
    row.append(named_folder)
    row.append(subdir)
    row.append(relpath)
    row.append(folder_count)
    row.append(folder_size)
    row.append(str(dict_filecount_sorted))
    row.append(str(dict_filesizes_sorted))
    row.append(str(dict_mimecount_sorted))
    row.append(str(dict_mimesizes_sorted))
    row.append(str(dict_extcount_sorted))
    row.append(str(dict_extsizes_sorted))

    allfiles.append(row)

### End of subdirs loop



# Convert to DataFrame
allfiles_df = pd.DataFrame(allfiles)

# Rename columns
allfiles_df.columns = ['named_folder', 'subdir', 'relpath', 'filecount', 'filesize', 'filecount_by_type', 'filesize_by_type', 'filecount_by_mimetype','filesize_by_mimetype', 'filecount_by_ext', 'filesize_by_ext']

allfiles_df.sort_values('filesize', ascending=False, inplace=True)

# Output to csv
allfiles_df.to_csv('output/00_catalogue_folder_level.csv', index=False)

# Print output to screen
print("Folder summary view run:")
print(allfiles_df[['subdir', 'filecount', 'filesize']])
print("\nSee output/00_catalogue_folder_level.csv for full detailed summary.\n")
