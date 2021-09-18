# py 3.9.7

"""
    CS528 - Data Privacy and Security
    Illinois Institute of Technology
    Homework 1
    9-17-21
    
    main.py
    
    The main of the hw script, it can take in an argument 1-5 to run
    the respective hw task
    
    Argument s outputs stats on the data used to create the hierarchy
"""

import sys

# Script must run in 3.9.x
assert sys.version_info >= (3, 9)

from Anon import anonymizeData, getDistortion, getPrecision, interpretData
from Stats import printAllStats

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


# print statistics about the data
def printStats():
    rawUsers: list

    with open("data/adult.data") as f:
        rawUsers = interpretData(f.read())

    printAllStats(rawUsers)


# main function that takes in arguments or manually set tasks
def main(manual: list[int] = None):
    tasks = (Task1, Task2c, Task2dI, Task2dII, Task2dIII)

    if len(sys.argv) > 1:
        if sys.argv[1][0] == "s":
            printStats()
            sys.exit()
        elif sys.argv[1].isdigit() and 0 < int(sys.argv[1]) <= len(tasks):
            tasks[int(sys.argv[1]) - 1]()
            sys.exit()

    if manual:
        for t in manual:
            tasks[t]()
        sys.exit()

    sys.exit(f"Give argument for task to run \n  Eg: {sys.argv[0]} [1-{len(tasks)}]\n\nOr arg 's' to print stats")


if __name__ == "__main__":
    main()