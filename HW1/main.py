from User import User


def interpretData(data: str):
    userList = list()
    for line in data.splitlines():
        args = line.split(",")
        if len(args) == 15:
            userList.append(User(*args))
    return userList


def kReached(userList):
    for user in userList:
        if not user.kReached():
            return False


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
            if not user.kReached():
                user.diverseAttr().upGenLevel()
                run = True

        workingUsers = groupedUsers

        print(f"Groups left: {len(workingUsers)}")

    print("Done")

    fnl = ""

    for user in workingUsers:
        fnl += str(user) + "\n"

    with open("out.data", "w") as f:
        f.write(fnl)


main()