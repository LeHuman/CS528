from User import User

def interpretData(data : str):
    userList = list()
    for line in data.splitlines():
        args = line.split(',')
        userList.append(User(*args))
    print(userList)