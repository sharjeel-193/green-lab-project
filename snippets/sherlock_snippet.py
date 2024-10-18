#This file contains a snippet of a loop taken from https://github.com/sherlock-project/sherlock (as of 24.09.2024)

import sys

#from sherlock.py, ln 152
def check_for_parameter(username):
    """checks if {?} exists in the username
    if exist it means that sherlock is looking for more multiple username"""
    return "{?}" in username

checksymbols = ["_", "-", "."]


def multiple_usernames(username):
    """replace the parameter with with symbols and return a list of usernames"""
    allUsernames = []
    for i in checksymbols:
        allUsernames.append(username.replace("{?}", i))
    return allUsernames


# added code for loop optimization testing
# this assumes that the usernames provided through the argument will have the "{?}" parameter. this is done to skip the additional check
def run_multiple_usernames():
    usernames = sys.argv[1].split("\n")
    # print(usernames)

    print(sys.argv[1])
    print(sys.argv[0])

#ln 827
    all_usernames = []
    for username in usernames:
        # if check_for_parameter(username):
        for name in multiple_usernames(username):
            all_usernames.append(name)
        # else:
        #     all_usernames.append(username)

    print("Total usernames: " + str(len(all_usernames)))

if __name__ == "__main__":
    run_multiple_usernames()
