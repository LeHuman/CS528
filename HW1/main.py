from User import User


def interpretData(data: str):
    userList = list()
    for line in data.splitlines():
        args = line.split(",")
        if len(args) == 15:
            userList.append(User(*args))
    return userList


def avgAge(userList: list):
    avg = 0
    for user in userList:
        avg += user.age
    return avg / len(userList)


def main():
    userList: list

    with open("Data/adult.data") as f:
        userList = interpretData(f.read())

    print(f"Avg Age: {avgAge(userList)}")


main()