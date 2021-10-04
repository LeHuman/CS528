# py 3.9.7

"""
    CS528 - Data Privacy and Security
    Illinois Institute of Technology
    Homework 2
    9-17-21
    
    main.py
    
    Local differential privacy
"""

import pandas as pd
import numpy as np

from pandas import DataFrame, Series
from math import exp


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


def LDP_RR(eps: float, users: DataFrame) -> Series:

    print(f"\n> Random Response | epsilon = {eps}")

    ages = users["age"]

    e = exp(eps)
    d = len(users)
    p = e / (e + d - 1)  # Ch.4 Slide 41
    q = 1 / (e + d - 1)  # Ch.4 Slide 41
    prob = normalize(Series((p, q), index=("True Answer", "False Answer")))

    print("\nProbabilites:")
    print(prob.to_string(), "\n")

    # "Client side"
    def RR(age: int) -> int:
        if np.random.choice(prob.keys(), p=prob) == "True Answer":
            return age
        else:
            return ages.sample().values[0]  # should be uniform for "any other value"

    agesR = ages.apply(lambda x: RR(x))
    agesResponse = agesR.value_counts()  # "Return" value of age distribution
    actual = ages.mean()

    # "Server side"
    def unbias(i_v: int) -> float:
        p, q = prob
        return (i_v - (len(agesResponse) * q)) / (p - q)  # Ch.4 Slide 41

    def unbiasedEstimate(ageDistr: Series) -> float:
        ageDistr = ageDistr.apply(unbias)
        avg = 0
        c = 0
        for age, count in ageDistr.items():
            c += count
            avg += age * count
        return avg / c

    returned = agesR.mean()
    unbiased = unbiasedEstimate(agesResponse)

    print(f"Actual:  {actual}")
    print(f"Return:  {returned}\t{round(100*(returned-actual)/actual,2)}%")
    print(f"Unbiased:{unbiased}\t{round(100*(unbiased-actual)/actual,2)}%")


# Main Function
def main():
    print("\nLocal differential privacy")

    # Make prob output look nicer
    pd.options.display.float_format = "{:20,.9f}".format

    users = pd.read_csv("dataset/adult.data", skipinitialspace=True)
    LDP_RR(1, users)


if __name__ == "__main__":
    main()