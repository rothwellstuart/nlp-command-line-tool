### intro.py ###
#
# Provides intro message


def check_for_exit(userinput, check_list):

    import sys

    if userinput in check_list:
        print("Exiting program.")
        sys.exit(0)


def print_welcome_message():
    print("WELCOME to the NLP command line tool demo!\n\n")
    print("Please choose from the following options:")
    print("Enter S or start to start the demo")
    print("Enter x, q or quit at any point to leave the demo.\n\n")



def user_input_validation(valid_list):

    userinput = input("\nEnter your selection:").upper()

    while userinput not in valid_list:
        print("Sorry, you selected an invalid option. Please select again:")
        userinput = input("\nEnter your selection:").upper()

    print("\nYou selected: ", userinput)

    return userinput



def select_dir(current_dir, quit_list):

    import os

    userinput = input("Enter the directory you want to analyse, or enter test-data for pre-canned demo data.\nN.B. your current directory is:\n" + current_dir + "\n:")
    check_for_exit(userinput, quit_list)

    while not (os.path.exists(userinput)):
        print("You selected: ", userinput)
        print("Sorry, you selected an invalid directory path. Please select again:")
        userinput = input("Enter the directory you want to analyse:").upper()
        check_for_exit(userinput, quit_list)

    print("\nAnalysing files in directory ", userinput, "...\n")

    return userinput
