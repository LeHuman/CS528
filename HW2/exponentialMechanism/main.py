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


def dpExpDataAvg(eps: float, users: pd.DataFrame):
    """
    Run exponential DP on most frequent "Education" query

    Args:
        eps (float): privacy parameter epsilon
        users (pd.DataFrame): dataframe of all users
    """

    sensitivity = 1 / eps
    common = users["education"].mode()[0]
    probabilities = users["education"].value_counts().apply(lambda x: 100 * x / len(users))

    print(f"\nepsilon = {eps}")
    print(f"Sensitivity : {sensitivity}")
    print(f"Actual : {common}")
    print(f"Probabilities : \n{probabilities.to_string()}")


# Main Function
def main():
    print("\nDP - Laplace Mechanism")

    users = pd.read_csv("dataset/adult.data", skipinitialspace=True)

    dpExpDataAvg(1, users)
    dpExpDataAvg(0.5, users)


if __name__ == "__main__":
    main()