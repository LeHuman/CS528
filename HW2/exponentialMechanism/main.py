# py 3.9.7

"""
    CS528 - Data Privacy and Security
    Illinois Institute of Technology
    Homework 2
    9-17-21
    
    main.py
    
    Example implementation of differential privacy using the exponential mechanism
"""

import pandas as pd
import numpy as np
from math import exp
from pandas.core.series import Series


def normalize(series: Series) -> Series:
    """
    Normalize values to 1

    Args:
        series (Series): series to normalize

    Returns:
        Series: series normalized to 1
    """
    for _ in range(2):  # first run leaves sum as 0.99?
        s = sum(series)
        series = series.apply(lambda x: x / s)
    return series


def dpExpDataAvg(eps: float, users: pd.DataFrame):
    """
    Run exponential DP on most frequent "Education" query

    Args:
        eps (float): privacy parameter epsilon
        users (pd.DataFrame): dataframe of all users
    """

    # calculate sensitivity by observing max difference between two sets differing by one user
    actual = users["education"].value_counts()
    minKey = actual[lambda x: x == min(actual)].keys()[0]
    minUser = users[lambda x: x["education"] == minKey].sample().index
    neighboor = users.drop(minUser)["education"].value_counts()

    sensitivity = max(abs(neighboor - actual))

    actual = normalize(actual)

    def utility(r):
        return 100 * actual[r]  # Selecting a more common attr returns higher util value

    # calculate probabilites
    probabilities = users["education"].value_counts()
    for r, _ in actual.items():
        probabilities[r] = exp((eps * utility(r)) / (2 * sensitivity))  # Ch.3 Slide 33 / Def 3.4
    # norm to 1
    probabilities = normalize(probabilities)
    # weighted random choice of attribute to return
    calc = np.random.choice(probabilities.keys(), p=probabilities)
    # get actual most common attribute
    actual = users["education"].mode()[0]

    print(f"\nepsilon = {eps}")
    print(f"Sensitivity : {sensitivity}")
    print(f"Actual : {actual}")
    print(f"Return : {calc}")
    print(f"Probabilities : \n{probabilities.to_string()}")


# Main Function
def main():
    print("\nDP - Laplace Mechanism")

    # Make prob output look nicer
    pd.options.display.float_format = "{:20,.10f}".format

    users = pd.read_csv("dataset/adult.data", skipinitialspace=True)

    dpExpDataAvg(1, users)
    dpExpDataAvg(0.5, users)


if __name__ == "__main__":
    main()