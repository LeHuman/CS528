# py 3.9.7

"""
    CS528 - Data Privacy and Security
    Illinois Institute of Technology
    Homework 2
    9-17-21
    
    main.py
    
    Implementation of differential privacy using the laplace mechanism
"""

import numpy as np


def getAges(datafile: str) -> list[int]:
    """
    Get ages from datafile

    Args:
        datafile (str): path to datafile

    Returns:
        list[int]: list of ages
    """
    fnl: list[int] = list()

    with open(datafile) as f:
        for line in f.readlines():
            try:
                fnl.append(int(line.split(",")[0]))
            except ValueError:
                pass

    return fnl


def dpLapDataAvg(eps: float, ages: list[int]):
    """
    Run laplace DP on age list

    Args:
        eps (float): privacy parameter epsilon
        ages (list[int]): list of ages
    """

    sensitivity = 1 / eps
    avg = np.average(ages)
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

    ages = getAges("dataset/adult.data")

    dpLapDataAvg(1, ages)
    dpLapDataAvg(0.5, ages)


if __name__ == "__main__":
    main()