# py 3.9.7

"""
    CS528 - Data Privacy and Security
    Illinois Institute of Technology
    Homework 2
    9-17-21
    
    main.py
    
    Implementation of differential privacy using the laplace mechanism
"""

import pandas as pd
import numpy as np


def dpLapDataAvg(eps: float, users: pd.DataFrame):
    """
    Run laplace DP on avg age query

    Args:
        eps (float): privacy parameter epsilon
        ages (list[int]): list of ages
    """

    users = users[users["age"] > 25]  # Only include those above 25

    # The sensitivity of a function f is the amount f's output changes when its input changes by 1
    sensitivity = 1 / eps
    avg = users["age"].mean()
    lap = np.random.laplace(0, sensitivity, 1)[0]
    var = 2 * (sensitivity) ** 2  # Ch.3 Slide 25

    print(f"\nepsilon = {eps}")
    print(f"Sensitivity : {sensitivity}")
    print(f"Noise : {lap}")
    print(f"Actual : {avg}")
    print(f"Return : {avg + lap}")
    print(f"Variance : {var}")


# Main Function
def main():
    print("\nDP - Laplace Mechanism")

    users = pd.read_csv("dataset/adult.data")

    dpLapDataAvg(1, users)
    dpLapDataAvg(0.5, users)


if __name__ == "__main__":
    main()