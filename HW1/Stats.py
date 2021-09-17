# py 3.9.6

"""
    CS528 - Data Privacy and Security
    Illinois Institute of Technology
    Homework 1
    9-15-21
    
    Stats.py
"""

import statistics

pd = None
try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError:
    pd = None


def printAgeStats(userList: list):
    ages = list()
    for user in userList:
        ages.append(user.age.value)

    print(f"Mean Age: {statistics.mean(ages)}")
    print(f"Median Age: {statistics.median(ages)}")

    if pd != None:
        s = pd.Series(ages)
        sx = s.plot.hist()
        sx.figure.savefig("ageStats.png")
        sx.clear()


education_values = (
    "Doctorate",
    "Assoc-voc",
    "Assoc-acdm",
    "Masters",
    "Bachelors",
    "Prof-school",
    "Some-college",
    "HS-grad",
    "12th",
    "11th",
    "10th",
    "9th",
    "7th-8th",
    "5th-6th",
    "1st-4th",
    "Preschool",
)


def printEducationStats(userList: list):
    eduBins = [0] * len(education_values)

    for user in userList:
        i = education_values.index(user.education.value)
        eduBins[i] += 1

    if pd != None:
        plt.xticks(rotation=90)
        s = pd.Series(data=eduBins, index=education_values)
        sx = s.plot.bar()
        sx.figure.tight_layout()
        sx.figure.savefig("educationStats.png")
        sx.clear()


matrial_values = [
    "Married-AF-spouse",
    "Married-civ-spouse",
    "Married-spouse-absent",
    "Separated",
    "Widowed",
    "Divorced",
    "Never-married",
]


def printMatrialStats(userList: list):
    marBins = [0] * len(matrial_values)

    for user in userList:
        i = matrial_values.index(user.marital_status.value)
        marBins[i] += 1

    if pd != None:
        plt.xticks(rotation=90)
        s = pd.Series(data=marBins, index=matrial_values)
        sx = s.plot.bar()
        sx.figure.tight_layout()
        sx.figure.savefig("matrialStats.png")
        sx.clear()


race_values = (
    "White",
    "Black",
    "Asian-Pac-Islander",
    "Amer-Indian-Eskimo",
    "Other",
)


def printRaceStats(userList: list):
    raceBins = [0] * len(race_values)

    for user in userList:
        i = race_values.index(user.race.value)
        raceBins[i] += 1

    if pd != None:
        plt.xticks(rotation=90)
        s = pd.Series(data=raceBins, index=race_values)
        sx = s.plot.bar()
        sx.figure.tight_layout()
        sx.figure.savefig("raceStats.png")
        sx.clear()