from User import User
from Interpret import interpretData

def main():
    with open("Data/adult.data") as f:
        userList = list()
        for line in f.readlines():
            args = line.strip('\n').split(',')
            if len(args) == 15:
                userList.append(User(*args))
        for user in userList:
            print(user)

main()