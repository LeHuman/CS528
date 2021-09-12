# py 3.9.6

"""
    Illinois Institute of Technology - CS528
    Data Privacy and Security
    Homework 1
    9-15-21
"""

from User import User

global_k = global_l = global_c = None  # defaults to user preference

# Force set diversity values on every user
# global_k = 5
# global_l = 3
# global_c = 0.5


def interpretData(data: str):  # 'cast' each user into User class
    userList = list()
    for line in data.splitlines():  # for each "user" aka each data line in adult.data
        args = line.split(",")
        if len(args) == 15:
            userList.append(User(*args, k=global_k, l=global_l, c=global_c))
    return userList


def condenseUsers(workingUsers: list) -> list:
    run = True
    last = len(workingUsers) + 1

    print(f"Condensing {last-1} blocks")

    while run:
        run = False
        workingList = workingUsers.copy()
        groupedUsers = list()

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


def printUserList(raw: list, users: list):
    print(f"Printing output of {len(users)} blocks")

    # output raw initial data

    fnl = ""

    for user in raw:
        fnl += user.basicStr() + "\n"

    with open("input.data", "w") as f:
        f.write(fnl)

    # output q-blocks

    fnl = ""

    with open("private_q-blocks.data", "w") as f:
        f.write(fnl)

    # output final data in a condensed format

    fnl = ""

    for user in users:
        fnl += user.toStr() + "\n"

    with open("out_condensed.data", "w") as f:
        f.write(fnl)

    # output final raw data

    fnl = ""

    for user in users:
        fnl += user.basicStr() + "\n"

    with open("out.data", "w") as f:
        f.write(fnl)

    size = getUserCount(users)

    print()
    print(f"Final User Count {size}/{len(raw)} : {round((100*size)/len(raw), 2)}%")
    print("\nTask 1(c)\n")
    print(f"\tAverage Distortion: {getDistortion(users)}")
    print(f"\tAverage Precision: {getPrecision(users)}")


def removeUnsatisfiedUsers(users: list[User]) -> list:
    finalUsers = list()
    for user in users:
        if user.satisfied():
            finalUsers.append(user)
    print(f"Removed {len(users) - len(finalUsers)} unsatisfied users from a total of {len(users)} users")
    return finalUsers


def getDistortion(users: list[User]) -> float:
    d = 0
    for user in users:
        d += user.getDistortion()
    return round(d / len(users), 4)


def getPrecision(users: list[User]) -> float:
    d = 0
    for user in users:
        d += user.getPrecision()
    return round(d / len(users), 4)


def getUserCount(users: list[User]) -> int:
    c = 0
    for user in users:
        c += user.count
    return c


def main():

    print(f"K:{global_k} L:{global_l} C:{global_c}\n")

    rawUsers: list

    print("Interpreting Data")
    # open data file and interpret each line as a user
    with open("Data/adult.data") as f:
        rawUsers = interpretData(f.read())

    # rawUsers = rawUsers[:5000]

    # condense users into q-blocks
    condensedUsers = condenseUsers(rawUsers.copy())

    while True:
        print("Checking for outliers")
        # extract outliers (where a user's occupation exists only once per q-block) and condense
        outliers = set()
        for user in condensedUsers:
            outliers = outliers.union(user.extractOutliers())

        # break loop is no more outliers have occurred or if unable to condense further
        if len(outliers) == 0:
            break

        print(f"Extracted {len(outliers)} outliers")

        print("Condensing outliers")
        # readd condensed outliers
        outliers = condenseUsers(list(outliers))
        removeUnsatisfiedUsers(outliers)
        condensedUsers.extend(outliers)

        if len(outliers) == 0:
            break

        # recondense after outliers have been re-added
        condensedUsers = condenseUsers(condensedUsers)

    print("Done with outliers")

    finalUsers = removeUnsatisfiedUsers(condensedUsers)

    printUserList(rawUsers, finalUsers)


main()