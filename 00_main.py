### Spine.py ###
#
# This is the main spine of the program flow
#
### N.B. to create executable:
# 1) pip install pyinstaller
# 2) pyinstaller --onefile <your_script_name>.py


# Imports
# import os, subprocess

# sys.path.append(".")
import os, sys
import localfunctions



### Initialise variables

# Valid user inputs
valid_userinput_quit = ['X', 'EXIT', 'Q', 'QUIT']
valid_userinput_start = ['S', 'START']

# Output directory
initial_dir = os.getcwd()
outdir = 'output'
archivedir = 'output/archive'

if not os.path.exists(outdir):
    os.makedirs(outdir)
if not os.path.exists(archivedir):
    os.makedirs(archivedir)

# Call intro message
# os.system("./01_intro.py")
# subprocess.Popen("./01_intro.py", shell=True)
# execfile("01_intro.py")
localfunctions.print_welcome_message()


# Take user response
user_input = localfunctions.user_input_validation(valid_userinput_quit + valid_userinput_start)

# Select directory to analyse
selected_dir = localfunctions.select_dir(initial_dir, valid_userinput_quit)

### Run cataloguing at folder level, on the selected directory
print("\nRunning on ", selected_dir, "\n")
# import catalogue_folder_level
with open("catalogue_folder_level.py","r") as rnf:
    exec(rnf.read())


### Run cataloguing at file level, on the selected directory
with open("catalogue_classification_file_level.py","r") as rnf:
    exec(rnf.read())

### Run entity extraction on eligible files
with open("entity_extraction_spacy.py","r") as rnf:
    exec(rnf.read())
