# py 3.9.6

"""
    Illinois Institute of Technology - CS528
    Data Privacy and Security
    Homework 1
    9-15-21
"""

import os
from Attr import TOTAL_ATTRIBUTES
from User import User
import sys

assert sys.version_info >= (3, 9)


# I/O

output_path = "output"


def printUserList(prefix: str, raw: list[User], users: list[User]):
    print(f"Printing output of {len(users)} blocks")

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


# 'cast' each user into User class
def interpretData(data: str, global_k: float = None, global_l: float = None, global_c: float = None):
    userList = list()
    for line in data.splitlines():  # for each "user" aka each data line in adult.data
        args = line.split(",")
        if len(args) == 15:
            userList.append(User(*args, k=global_k, l=global_l, c=global_c))
    return userList


# Condensers


def condenseUsers(workingUsers: list[User]) -> list[User]:
    run = True
    last = len(workingUsers) + 1

    print(f"Condensing {last-1} blocks")

    while run:
        run = False
        workingList: list[User] = workingUsers.copy()
        groupedUsers: list[User] = list()

        while len(workingList) != 0:
            u = workingList.pop()
            if not u or u.generalized():
                continue

            i = 0
            for user in workingList:
                if u.add(user):
                    workingList[i] = None
                i += 1

            groupedUsers.append(u)

        if len(groupedUsers) == last:
            print("Unable to further generalize")
            workingUsers = groupedUsers
            break
        last = len(groupedUsers)

        for user in groupedUsers:
            if not user.satisfied():
                user.diverseAttr().upGenLevel()
                run = True

        workingUsers = groupedUsers

        print(f"q*-blocks: {len(workingUsers)}")

    print(f"Done: {len(workingUsers)}")
    return workingUsers


def removeUnsatisfiedUsers(users: list[User]) -> list:
    finalUsers = list()
    for user in users:
        if user.satisfied():
            finalUsers.append(user)
    if len(users) != len(finalUsers):
        print(f"Removed {len(users) - len(finalUsers)} unsatisfied users from a total of {len(users)} users")
    return finalUsers


# Not Used
def removeOutliers(users: list[User]) -> list[User]:
    while True:
        print("Checking for outliers")
        # extract outliers (where a user's occupation exists only once per q*-block) and condense
        outliers = set()
        for user in users:
            outliers = outliers.union(user.extractOutliers())

        # break loop is no more outliers have occurred or if unable to condense further
        if len(outliers) == 0:
            break

        print(f"Extracted {len(outliers)} outliers")

        print("Condensing outliers")
        # readd condensed outliers
        outliers = condenseUsers(list(outliers))
        removeUnsatisfiedUsers(outliers)
        users.extend(outliers)

        if len(outliers) == 0:
            break

        # recondense after outliers have been re-added
        users = condenseUsers(users)
    print("Done with outliers")
    return users


# Qualifiers


def getDistortion(users: list[User]) -> float:
    d = 0
    for user in users:
        d += user.getDistortion()
    return round(d / len(users), 4)


def getPrecision(users: list[User]) -> float:
    d = 0
    for user in users:
        d += user.getPrecisionNumerator()
    return round(1 - (d / (getUserCount(users) * TOTAL_ATTRIBUTES)), 4)


def getUserCount(users: list[User]) -> int:
    c = 0
    for user in users:
        c += user.count
    return c


# Logic


def anonymizeData(name: str, k: float = None, l: float = None, c: float = None) -> list[User]:
    print(f"K:{k} L:{l} C:{c}\n")

    rawUsers: list

    print("Interpreting Data")

    # open data file and interpret each line as a user
    with open("data/adult.data") as f:
        rawUsers = interpretData(f.read(), k, l, c)

    rawUsers = rawUsers[:1000]

    # condense users into q*-blocks
    condensedUsers = condenseUsers(rawUsers.copy())

    # remove outliers
    # condensedUsers = removeOutliers(condensedUsers)

    # remove users / blocks that do not meet criterial
    finalUsers = removeUnsatisfiedUsers(condensedUsers)

    printUserList(name, rawUsers, finalUsers)
    return finalUsers


def main():

    print("Running Task 1")

    task1Users = anonymizeData("Task1")

    print("\nTask 1 (c)\n")
    print(f"\tAverage Distortion: {getDistortion(task1Users)}")
    print(f"\tAverage Precision: {getPrecision(task1Users)}")

    print("Running Task 2 (c)")

    task1Users = anonymizeData("Task2c", 5, 3)

    print("\nTask 2 (c)\n")
    print(f"\tAverage Distortion: {getDistortion(task1Users)}")
    print(f"\tAverage Precision: {getPrecision(task1Users)}")

    print("Running Task 2 (d) I")

    task1Users = anonymizeData("Task2dI", 5, 3, 0.5)

    print("\nTask 2 (d) I\n")
    print(f"\tAverage Distortion: {getDistortion(task1Users)}")
    print(f"\tAverage Precision: {getPrecision(task1Users)}")

    print("Running Task 2 (d) II")

    task1Users = anonymizeData("Task2dII", 5, 3, 1)

    print("\nTask 2 (d) II\n")
    print(f"\tAverage Distortion: {getDistortion(task1Users)}")
    print(f"\tAverage Precision: {getPrecision(task1Users)}")

    print("Running Task 2 (d) III")

    task1Users = anonymizeData("Task2dIII", 5, 3, 2)

    print("\nTask 2 (d) III\n")
    print(f"\tAverage Distortion: {getDistortion(task1Users)}")
    print(f"\tAverage Precision: {getPrecision(task1Users)}")


main()