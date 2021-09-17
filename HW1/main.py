# py 3.9.6

"""
    CS528 - Data Privacy and Security
    Illinois Institute of Technology
    Homework 1
    9-15-21
    
    main.py
"""

import os
import gc
import sys

from Stats import printAllStats
from Attr import TOTAL_ATTRIBUTES
from User import User

assert sys.version_info >= (3, 9)


# I/O

# Where to output the results
output_path = "output"

# Print out the input and output data post anonymization
# NOTE: only Task*_out.data within it's respective folder in output_path is the actual anonymized data, other outputs are only used for analyzing this implementation
def printUserList(prefix: str, raw: list[User], users: list[User]):
    print(f"Printing output of {len(users)} blocks")

    # make directories that are needed

    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    path = os.path.join(output_path, prefix)

    if not os.path.isdir(path):
        os.mkdir(path)

    # output initial filtered data

    fnl = ""

    for user in raw:
        fnl += user.privateStr(True) + "\n"

    with open(os.path.join(path, f"{prefix}_input.data"), "w") as f:
        f.write(fnl)

    # output private data in final q*-blocks

    fnl = ""

    for user in users:
        fnl += user.privateStr() + "\n"

    with open(os.path.join(path, f"{prefix}_input_condensed.data"), "w") as f:
        f.write(fnl)

    # output final raw data

    fnl = ""

    for user in users:
        fnl += user.basicStr() + "\n"

    with open(os.path.join(path, f"{prefix}_out.data"), "w") as f:
        f.write(fnl)

    # output final data in a condensed format

    fnl = ""

    for user in users:
        fnl += user.toStr() + "\n"

    with open(os.path.join(path, f"{prefix}_out_condensed.data"), "w") as f:
        f.write(fnl)

    # print final stats

    size = getUserCount(users)

    print()
    print(f"Final User Count {size}/{len(raw)} : {round((100*size)/len(raw), 2)}%")


# 'convert' each user into a User class
def interpretData(data: str, global_k: float = None, global_l: float = None, global_c: float = None):
    userList = list()
    for line in data.splitlines():  # for each "user" aka each data line in adult.data
        args = line.split(",")
        if len(args) == 15:
            userList.append(User(*args, k=global_k, l=global_l, c=global_c))
    return userList


# Condensers

# Match each user to a similar user, continuously generalizting their attributes until
# each user is satisfied, or if users are no longer matching
def condenseUsers(workingUsers: list[User]) -> list[User]:
    # Whether to keep running
    run = True
    # Keep track of the groups, if it does not change this means we are stagnating
    last = len(workingUsers) + 1

    print(f"Condensing {last-1} blocks")

    # Keep track of users lost due to complete generalization
    generalized = 0

    while run:
        run = False
        # copy of working list to be iterated over
        workingList: list[User] = workingUsers.copy()
        # The new list of grouped users
        groupedUsers: list[User] = list()

        while len(workingList) != 0:
            u = workingList.pop()  # take out a user
            if not u:  # if it was not set to None, go on
                continue
            if u.generalized():  # if it is not completely generalized, go on
                generalized += u.count
                continue

            i = 0
            for user in workingList:  # compare u with each other user, grouping them if matched
                if u.add(user):
                    workingList[i] = None  # because this user is now under another user, set it's reference in workingList to None
                i += 1

            groupedUsers.append(u)  # add user / q*-block to new list

        # If size does not change, we are stagnating, stop
        if len(groupedUsers) == last:
            print("Unable to further generalize")
            workingUsers = groupedUsers
            gc.collect()
            break
        last = len(groupedUsers)

        # For all users in the new list, if anyone is not satisfied,
        # generalize an attribute then continue
        for user in groupedUsers:
            if not user.satisfied():
                user.diverseAttr().upGenLevel()
                run = True

        # replace new list
        workingUsers = groupedUsers

        gc.collect()

        print(f"q*-blocks: {len(workingUsers)}")

    print(f"Done: {len(workingUsers)}")
    print(f"Users: {getUserCount(workingUsers)}")
    print(f"Users Lost: {generalized}")
    return workingUsers


# Remove any users / q*-blocks that may be unsatisfied. This ensures the final critera for the Table is met
def removeUnsatisfiedUsers(users: list[User]) -> list:
    finalUsers = list()
    for user in users:
        if user.satisfied():
            finalUsers.append(user)
    if len(users) != len(finalUsers):
        print(f"Removed {len(users) - len(finalUsers)} unsatisfied users from a total of {len(users)} users")
    return finalUsers


# NOTE: Not Used
# def removeOutliers(users: list[User]) -> list[User]:
#     while True:
#         print("Checking for outliers")
#         # extract outliers (where a user's occupation exists only once per q*-block) and condense
#         outliers = set()
#         for user in users:
#             outliers = outliers.union(user.extractOutliers())

#         # break loop is no more outliers have occurred or if unable to condense further
#         if len(outliers) == 0:
#             break

#         print(f"Extracted {len(outliers)} outliers")

#         print("Condensing outliers")
#         # readd condensed outliers
#         outliers = condenseUsers(list(outliers))
#         removeUnsatisfiedUsers(outliers)
#         users.extend(outliers)

#         if len(outliers) == 0:
#             break

#         # recondense after outliers have been re-added
#         users = condenseUsers(users)
#     print("Done with outliers")
#     return users


# Qualifiers

# Get a table's average distortion
def getDistortion(users: list[User]) -> float:
    d = 0
    for user in users:
        d += user.getDistortion()
    return round(d / len(users), 4)


# Get a table's average percision
def getPrecision(users: list[User]) -> float:
    d = 0
    for user in users:
        d += user.getPrecisionNumerator()
    return round(1 - (d / (getUserCount(users) * TOTAL_ATTRIBUTES)), 4)


# Get a table's total count of users
def getUserCount(users: list[User]) -> int:
    c = 0
    for user in users:
        c += user.count
    return c


# Logic


def anonymizeData(name: str, k: float = None, l: float = None, c: float = None) -> list[User]:
    print(f"{name} K:{k} L:{l} C:{c}\n")

    rawUsers: list

    print(f"{name} Interpreting Data")

    # open data file and interpret each line as a user
    with open("data/adult.data") as f:
        rawUsers = interpretData(f.read(), k, l, c)

    # condense users into q*-blocks
    condensedUsers = condenseUsers(rawUsers.copy())

    # remove outliers
    # condensedUsers = removeOutliers(condensedUsers)

    # remove users / blocks that do not meet criterial
    finalUsers = removeUnsatisfiedUsers(condensedUsers)

    # print out results
    printUserList(name, rawUsers, finalUsers)
    return finalUsers


# Tasks


def Task1():
    print("Running Task 1")

    task1Users = anonymizeData("Task1")

    print("\nTask 1 (c)\n")
    print(f"\tAverage Distortion: {getDistortion(task1Users)}")
    print(f"\tAverage Precision: {getPrecision(task1Users)}")


def Task2c():
    print("Running Task 2 (c)")

    task1Users = anonymizeData("Task2c", 5, 3)

    print("\nTask 2 (c)\n")
    print(f"\tAverage Distortion: {getDistortion(task1Users)}")
    print(f"\tAverage Precision: {getPrecision(task1Users)}")


def Task2dI():
    print("Running Task 2 (d) I")

    task1Users = anonymizeData("Task2dI", 5, 3, 0.5)

    print("\nTask 2 (d) I\n")
    print(f"\tAverage Distortion: {getDistortion(task1Users)}")
    print(f"\tAverage Precision: {getPrecision(task1Users)}")


def Task2dII():
    print("Running Task 2 (d) II")

    task1Users = anonymizeData("Task2dII", 5, 3, 1)

    print("\nTask 2 (d) II\n")
    print(f"\tAverage Distortion: {getDistortion(task1Users)}")
    print(f"\tAverage Precision: {getPrecision(task1Users)}")


def Task2dIII():
    print("Running Task 2 (d) III")

    task1Users = anonymizeData("Task2dIII", 5, 3, 2)

    print("\nTask 2 (d) III\n")
    print(f"\tAverage Distortion: {getDistortion(task1Users)}")
    print(f"\tAverage Precision: {getPrecision(task1Users)}")


def printStats():
    rawUsers: list

    with open("data/adult.data") as f:
        rawUsers = interpretData(f.read())

    printAllStats(rawUsers)


def main():
    tasks = (Task1, Task2c, Task2dI, Task2dII, Task2dIII)

    if len(sys.argv) > 1:
        try:
            if sys.argv[1][0] == "s":
                printStats()
                sys.exit()
            elif 0 < int(sys.argv[1]) <= len(tasks):
                tasks[int(sys.argv[1]) - 1]()
                sys.exit()
        except ValueError:
            pass

    sys.exit(f"Give argument for task to run \n  Eg: {sys.argv[0]} [1-{len(tasks)}]\n\nOr arg 's' to print stats")


if __name__ == "__main__":
    main()