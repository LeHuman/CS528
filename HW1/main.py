from User import User


def interpretData(data: str):
    userList = list()
    for line in data.splitlines():
        args = line.split(",")
        userList.append(User(*args))
    print(userList)


def main():
    with open("Data/adult.data") as f:
        userList = list()
        for line in f.readlines():
            args = line.strip("\n").split(",")
            if len(args) == 15:
                userList.append(User(*args))
        for user in userList:
            print(user)


main()