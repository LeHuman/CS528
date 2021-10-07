# py 3.9.7

"""
    CS528 - Data Privacy and Security
    Illinois Institute of Technology
    Homework 2
    9-17-21
    
    main.py
    
    Differentially Private Classification using iris dataset
"""

import pandas as pd
import numpy as np
from scipy.stats import norm
from pandas.core.frame import DataFrame
from pandas.core.series import Series


def input2S(sepal_length, sepal_width, petal_length, petal_width) -> Series:
    return Series(data={"sepal-length": sepal_length, "sepal-width": sepal_width, "petal-length": petal_length, "petal-width": petal_width})


def filterDataset(classData: DataFrame, _=None) -> DataFrame:
    classData = classData.drop("class", axis=1)
    return DataFrame(data={"mean": classData.mean(), "std": classData.std()})


def lapNoiseAVG(eps, n):
    sensitivity = (1 / n) / eps
    return np.random.laplace(0, sensitivity, 1)[0]


def dpLAPData(classData: DataFrame, eps: float) -> DataFrame:
    df = filterDataset(classData)
    df = df.applymap(lambda x: x + lapNoiseAVG(eps, len(classData)))
    return df


class Flower:
    df: DataFrame = None
    cls = ""
    n = 0

    def __init__(self, cls: str, n: int, classStats: DataFrame) -> None:
        self.cls = cls
        self.n = n
        self.df = classStats

    def __str__(self) -> str:
        return self.df.to_string()

    def gaussianProb(self, entry: Series) -> float:
        p = 1.0
        for i, stat in self.df.iterrows():
            p *= norm.pdf(entry[i], stat["mean"], stat["std"])
        return p


def classProb(entry: Series, flowers: list[Flower]) -> dict[str, float]:
    n = int(sum([f.n for f in flowers]))
    probabilities = dict()
    for flower in flowers:
        probabilities[flower.cls] = flower.gaussianProb(entry) * flower.n / n
    return probabilities


def predictClass(dimensions: Series, flowers: list[Flower]) -> str:
    prob = classProb(dimensions, flowers)
    return max(prob.items(), key=lambda x: x[1])[0]


# Main Function
def main():
    print("\nDifferentially Private Classification\n")

    flowers = pd.read_csv("dataset/iris.data")

    setosas = flowers[flowers["class"] == "Iris-setosa"]
    versicolours = flowers[flowers["class"] == "Iris-versicolor"]
    virginicas = flowers[flowers["class"] == "Iris-virginica"]

    tests = (
        (flowers[1:11].drop("class", axis=1), flowers["class"][1]),
        (flowers[51:61].drop("class", axis=1), flowers["class"][51]),
        (flowers[101:111].drop("class", axis=1), flowers["class"][101]),
    )

    flowers = [setosas, versicolours, virginicas]

    for i in range(len(flowers)):
        cls = flowers[i]
        flowers[i] = Flower(cls["class"].values[0], len(cls), dpLAPData(cls, 1))

    for sets, actual in tests:
        i = 0
        for set in sets.iterrows():
            i += 1 if predictClass(set[1], flowers) == actual else 0
        print(f"{actual} percision = {round(100 * i / len(sets), 2)}%")


if __name__ == "__main__":
    main()