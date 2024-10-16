#This file contains the code snippet taken from "Sherlock" with the loop in multiple_usernames unrolled

import sys

#from sherlock.py, ln 152
def check_for_parameter(username):
    """checks if {?} exists in the username
    if exist it means that sherlock is looking for more multiple username"""
    return "{?}" in username

checksymbols = ["_", "-", "."]

#multiple_usernames unrolled
def multiple_usernames_unrolled(username):
    allUsernames = []
    #unrolled loop
    allUsernames.append(username.replace("{?}", "_"))
    allUsernames.append(username.replace("{?}", "-"))
    allUsernames.append(username.replace("{?}", "."))

    return allUsernames

# added code for loop optimization testing
# this assumes that the usernames provided through the argument will have the "{?}" parameter. this is done to skip the additional check
def run_multiple_usernames():
    usernames = sys.argv[1].split("\n")

#ln 827
    all_usernames = []
    for username in usernames:
        # if check_for_parameter(username):
        for name in multiple_usernames_unrolled(username):
            all_usernames.append(name)
        # else:
        #     all_usernames.append(username)

    print("Total usernames: " + str(len(all_usernames)))

if __name__ == "__main__":
    run_multiple_usernames()
    
