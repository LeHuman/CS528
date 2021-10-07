# py 3.9.7

"""
    CS528 - Data Privacy and Security
    Illinois Institute of Technology
    Homework 2
    9-17-21
    
    main.py
    
    Local differential privacy
"""

from functools import reduce
from types import FunctionType
from typing import Iterable, Iterator
from multiprocessing import Pool
from pandas import DataFrame, Series
from math import exp

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Config
DATA_PATH = "dataset/adult.data"
VAL_ROUND = 6
USER_PERCENT_RANGE = 100
EPSILON_RANGE = 10


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


def LDP_RR(eps: float, users: DataFrame) -> tuple:

    # Used for multiprocessed output
    global rtnMsg
    rtnMsg = ""

    def print(msg: str) -> None:
        global rtnMsg
        rtnMsg += msg + "\n"

    print(f"\n> Random Response | epsilon = {eps}")

    ages = users["age"]

    e = exp(eps)
    # d = len(ages.value_counts().keys())  # d = possible values
    d = len(ages)
    p = e / (e + d - 1)  # Ch.4 Slide 41
    q = 1 / (e + d - 1)  # Ch.4 Slide 41
    prob = normalize(Series((p, q), index=("True Answer", "False Answer")))

    print("\nProbabilites:")
    print(prob.to_string() + "\n")

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
        # p, q = prob
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

    print(f"Actual:  {round(actual, VAL_ROUND)}")
    print(f"Return:  {round(returned, VAL_ROUND)}")
    print(f"Unbiased:{round(unbiased, VAL_ROUND)}")

    return (rtnMsg, eps, len(users), unbiased)


class UnaryEncoding(list):
    val: int = -1

    @classmethod
    def from_list(cls, list: list[int]):
        UE = UnaryEncoding()
        UE.extend(list)
        return UE

    def __init__(self, decimal: int = None, pad: int = None) -> None:
        super().__init__()
        if decimal == None:
            return
        self.val = decimal
        binaryStr = bin(decimal)[2:]
        for bit in binaryStr:
            self.append(int(bit))
        if pad:
            a = self.__pad(self, pad)
            self.clear()
            self.extend(a)

    def copy(self) -> list[int]:
        return self.from_list(super().copy())

    def apply(self, function: FunctionType) -> list[int]:
        i = 0
        cpy = self.copy()
        for b in self:
            cpy[i] = function(b)
            i += 1
        return cpy

    def __pad(self, x: list[int], l: int) -> list[int]:
        r = (l * [0]) + x
        return r[len(r) - l :]

    def __add(self, y: list[int], add=True) -> list[int]:
        l = max(len(self), len(y))
        x = self.__pad(self, l)
        y = self.__pad(y, l)

        fnl = UnaryEncoding()
        for i in range(l):
            if add:
                fnl.append(x[i] + y[i])
            else:
                fnl.append(x[i] - y[i])
        return fnl

    def __sub__(self, y: list[int]) -> list[int]:
        return self.__add(y, False)

    def __add__(self, y: list[int]) -> list[int]:
        return self.__add(y)

    def __str__(self) -> str:
        if self.val < 0:
            return super().__str__() + " UE"
        return super().__str__() + " = " + str(self.val)


def LDP_UE(eps: float, users: DataFrame) -> tuple:

    # Used for multiprocessed output
    global rtnMsg
    rtnMsg = ""

    def print(msg: str) -> None:
        global rtnMsg
        rtnMsg += msg + "\n"

    print(f"\n> Unary Encoding | epsilon = {eps}")

    e = exp(eps / 2)
    p = e / (e + 1)  # Ch.4 Slide 43
    q = 1 / (e + 1)  # Ch.4 Slide 43
    prob = normalize(Series((p, q), index=("Keep", "Flip")))
    p, q = prob
    n = len(users)

    print("\nProbabilites:")
    print(prob.to_string() + "\n")

    # "Client side"
    def UE(bit: int) -> int:
        if np.random.choice(prob.keys(), p=prob) == "Keep":
            return bit
        else:
            return 1 if bit == 0 else 0

    uAges = list(set(users["age"]))
    uAges.sort()

    binAges = dict()
    for i in range(len(uAges)):
        binAges[uAges[i]] = UnaryEncoding(1 << i, len(uAges))

    ages = users["age"].apply(lambda x: binAges[x])
    agesEncodedActual: DataFrame = reduce(lambda x, y: x + y, ages)
    agesEncodedActual = Series(agesEncodedActual[::-1])

    ages = ages.apply(lambda x: x.apply(UE))
    agesEncodedReturn: DataFrame = reduce(lambda x, y: x + y, ages)  # "Return" value
    agesEncodedReturn = Series(agesEncodedReturn[::-1])

    # "Server side"

    def unbias(i_v: int) -> int:
        return (i_v - (n * q)) / (p - q)  # Ch.4 Slide 41

    agesEncodedUnBiased: Series = agesEncodedReturn.apply(unbias)

    for i in range(len(agesEncodedActual)):
        agesEncodedActual[i] *= uAges[i]
        agesEncodedReturn[i] *= uAges[i]
        agesEncodedUnBiased[i] *= uAges[i]

    actual = sum(agesEncodedActual) / n
    returned = sum(agesEncodedReturn) / n
    unbiased = sum(agesEncodedUnBiased) / n

    print(f"Actual:  {round(actual, VAL_ROUND)}")
    print(f"Return:  {round(returned, VAL_ROUND)}")
    print(f"Unbiased:{round(unbiased, VAL_ROUND)}")

    return (rtnMsg, eps, len(users), unbiased)


# Main Function
def main():
    print("\nLocal differential privacy")

    # Make prob output look nicer
    pd.options.display.float_format = ("{" + f":10,.{VAL_ROUND}f" + "}").format

    global users
    users = pd.read_csv(DATA_PATH, skipinitialspace=True)

    actual = users["age"].mean()

    print("----[ Task 4(b) ]----")

    UEEst = [0] * EPSILON_RANGE
    RREst = [0] * EPSILON_RANGE

    with Pool(EPSILON_RANGE) as p:
        for msg in p.starmap(LDP_UE, [(i, users) for i in range(1, EPSILON_RANGE + 1)]):
            print(msg[0])
            UEEst[msg[1] - 1] = msg[3]
        for msg in p.starmap(LDP_RR, [(i, users) for i in range(1, EPSILON_RANGE + 1)]):
            print(msg[0])
            RREst[msg[1] - 1] = msg[3]

    UEEst_E = [round(abs(e - actual), VAL_ROUND) for e in UEEst]
    RREst_E = [round(abs(e - actual), VAL_ROUND) for e in RREst]
    x = list(range(1, EPSILON_RANGE + 1))

    plt.style.use("dark_background")
    fig, ax = plt.subplots()
    UE_patch = mpatches.Patch(color="red", label="Unary Encoding")
    RR_patch = mpatches.Patch(color="blue", label="Random Response")
    plt.legend(handles=[UE_patch, RR_patch])
    ax.set_xlabel("Epsilon")
    ax.set_ylabel("L_1 - distance (Age)")
    ax.set_title("LDP Error Frequency (Avg Age)")
    plt.plot(x, UEEst_E, "ro-")
    plt.plot(x, RREst_E, "bo-")
    fig.savefig("LDP/error_plot_eps.png")

    print("----[ Task 4(c) ]----")

    nDiffC = int(USER_PERCENT_RANGE / 10)
    eps = 2
    n = len(users)
    n10 = int(n * 0.1)
    nMax = int(n * USER_PERCENT_RANGE / 100) + 1

    UEEst = [0] * nDiffC
    RREst = [0] * nDiffC

    with Pool(nDiffC) as p:
        for msg in p.starmap(LDP_UE, [(eps, users[:i]) for i in range(n10, nMax, n10)]):
            print(msg[0])
            UEEst[int(msg[2] / n10) - 1] = msg[3]
        for msg in p.starmap(LDP_RR, [(eps, users[:i]) for i in range(n10, nMax, n10)]):
            print(msg[0])
            RREst[int(msg[2] / n10) - 1] = msg[3]

    UEEst_E = [round(abs(e - actual), VAL_ROUND) for e in UEEst]
    RREst_E = [round(abs(e - actual), VAL_ROUND) for e in RREst]
    x = list(range(n10, nMax, n10))

    plt.figure()
    plt.style.use("dark_background")
    fig, ax = plt.subplots()
    UE_patch = mpatches.Patch(color="red", label="Unary Encoding")
    RR_patch = mpatches.Patch(color="blue", label="Random Response")
    plt.legend(handles=[UE_patch, RR_patch])
    ax.set_xlabel("# of Users")
    ax.set_ylabel("L_1 - distance (Age)")
    ax.set_title("LDP Error Frequency (Avg Age)")
    plt.plot(x, UEEst_E, "ro-")
    plt.plot(x, RREst_E, "bo-")
    fig.savefig("LDP/error_plot_num.png")


if __name__ == "__main__":
    main()