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


def main():
    rawUsers: list

    with open("Data/adult.data") as f:
        rawUsers = interpretData(f.read())

    workingUsers = rawUsers.copy()

    run = True

    while run:
        run = False
        workingList = workingUsers.copy()
        groupedUsers = list()

        while len(workingList) != 0:
            u = workingList.pop()
            if not u:
                continue

            i = 0
            for user in workingList:
                if u.add(user):
                    workingList[i] = None
                i += 1

            groupedUsers.append(u)

        if len(workingUsers) == len(groupedUsers):
            workingUsers = groupedUsers
            break

        for user in groupedUsers:
            if not user.satisfied():
                user.diverseAttr().upGenLevel()
                run = True

        workingUsers = groupedUsers

        print(f"q*-blocks: {len(workingUsers)}")

    print(f"Done: {len(workingUsers)}")

    # output q-blocks

    fnl = ""

    for user in workingUsers:
        fnl += user.privateStr() + "\n"

    with open("private_q-blocks.data", "w") as f:
        f.write(fnl)

    # output final data in a condensed format

    fnl = ""

    for user in workingUsers:
        fnl += str(user) + "\n"

    with open("out_condensed.data", "w") as f:
        f.write(fnl)

    # output final raw data

    fnl = ""

    for user in workingUsers:
        fnl += user.basicStr() + "\n"

    with open("out.data", "w") as f:
        f.write(fnl)


main()