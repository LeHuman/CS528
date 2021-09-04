# import Stats
from random import randint as rnd
from User import User


def interpretData(data: str):
    userList = list()
    for line in data.splitlines():
        args = line.split(",")
        if len(args) == 15:
            userList.append(User(*args))
    return userList


def main():
    userList: list

    with open("Data/adult.data") as f:
        userList = interpretData(f.read())

    # Stats.printAgeStats(userList)
    # Stats.printEducationStats(userList)
    # Stats.printMatrialStats(userList)
    # Stats.printRaceStats(userList)


main()