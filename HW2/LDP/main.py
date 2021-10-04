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


def LDP_RR(eps: float, users: DataFrame) -> None:

    print(f"\n> Random Response | epsilon = {eps}")

    ages = users["age"]

    e = exp(eps)
    # d = len(ages.value_counts().keys())  # d = possible values
    d = len(ages)
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

    print(f"Actual:  {actual}")
    print(f"Return:  {returned}\t{round(100*(returned-actual)/actual,2)}%")
    print(f"Unbiased:{unbiased}\t{round(100*(unbiased-actual)/actual,2)}%")


class UnaryEncoding(list):
    val: int = -1

    @classmethod
    def from_list(cls, list: list[int]):
        UE = UnaryEncoding()
        UE.extend(list)
        return UE

    def __init__(self, decimal: int = None) -> None:
        super().__init__()
        if not decimal:
            return
        self.val = decimal
        binaryStr = bin(decimal)[2:]
        for bit in binaryStr:
            self.append(int(bit))

    def copy(self) -> list[int]:
        return self.from_list(super().copy())

    def apply(self, function: FunctionType) -> list[int]:
        i = 0
        cpy = self.copy()
        for b in self:
            cpy[i] = function(b)
            i += 1
        return cpy

    def compare(self, y: list[int]) -> float:
        assert len(self) == len(y)  # Cannot compare UEs with differing sizes
        diff: UnaryEncoding = self - y
        for i in range(len(diff)):
            diff[i] = diff[i] / self[i]
        return round(100 * sum(diff) / len(self), 2)

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


def LDP_UE(eps: float, users: DataFrame) -> None:
    print(f"\n> Unary Encoding | epsilon = {eps}")

    e = exp(eps / 2)
    p = e / (e + 1)  # Ch.4 Slide 43
    q = 1 / (e + 1)  # Ch.4 Slide 43
    prob = normalize(Series((p, q), index=("Keep", "Flip")))
    p, q = prob

    print("\nProbabilites:")
    print(prob.to_string(), "\n")

    # "Client side"
    def UE(bit: int) -> int:
        if np.random.choice(prob.keys(), p=prob) == "Keep":
            return bit
        else:
            return 1 if bit == 0 else 0

    ages = users["age"].apply(lambda x: UnaryEncoding(x))
    agesEncodedActual: UnaryEncoding = reduce(lambda x, y: x + y, ages)
    ages = ages.apply(lambda x: x.apply(UE))
    agesEncodedReturn: UnaryEncoding = reduce(lambda x, y: x + y, ages)  # "Return" value

    # "Server side"

    # global _i
    # _i = 0
    n = len(agesEncodedReturn)

    def unbias(i_v: int) -> int:
        # global _i
        # v = agesEncodedActual[_i]
        # i = agesEncodedReturn[_i]
        # _i += 1
        # n = (-2 * v * p + v + i) / q
        # print(n / len(users))
        # print(round(n), round(v - n))
        # n = i_v * 2
        return round((i_v - (n * q)) / (p - q))  # Ch.4 Slide 41

    agesEncodedUnBiased: UnaryEncoding = agesEncodedReturn.apply(unbias)

    print(f"Actual:  {agesEncodedActual}")
    print(f"Return:  {agesEncodedReturn} {agesEncodedActual.compare(agesEncodedReturn)}%")
    print(f"Unbiased:{agesEncodedUnBiased} {agesEncodedActual.compare(agesEncodedUnBiased)}%")


# Main Function
def main():
    print("\nLocal differential privacy")

    # Make prob output look nicer
    pd.options.display.float_format = "{:20,.9f}".format

    users = pd.read_csv("dataset/adult.data", skipinitialspace=True)
    LDP_UE(1, users)


if __name__ == "__main__":
    main()