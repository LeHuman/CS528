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


def input_entry(sepal_length, sepal_width, petal_length, petal_width) -> Series:
    d = {
        "sepal-length": sepal_length,
        "sepal-width": sepal_width,
        "petal-length": petal_length,
        "petal-width": petal_width,
    }
    return Series(data=d)


def filter_dataset(classData: DataFrame, _=None) -> DataFrame:
    classData = classData.drop("class", axis=1)
    return DataFrame(data={"mean": classData.mean(), "std": classData.std()})


def noise_LAP_AVG(eps, n):
    sensitivity = (1 / n) / eps
    return np.random.laplace(0, sensitivity, 1)[0]


def dp_data_LAP(classData: DataFrame, eps: float) -> DataFrame:
    df = filter_dataset(classData)
    df = df.applymap(lambda x: x + noise_LAP_AVG(eps, len(classData)))
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

    def gaussian_prob(self, entry: Series) -> float:
        p = 1.0
        for i, stat in self.df.iterrows():
            p *= norm.pdf(entry[i], stat["mean"], stat["std"])
        return p


def class_prob(entry: Series, flowers: list[Flower]) -> dict[str, float]:
    n = int(sum([f.n for f in flowers]))
    probabilities = dict()
    for flower in flowers:
        probabilities[flower.cls] = flower.gaussian_prob(entry) * flower.n / n
    return probabilities


def predict_class(dimensions: Series, flowers: list[Flower]) -> str:
    prob = class_prob(dimensions, flowers)
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

    flowers = [Flower(cls["class"].values[0], len(cls), dp_data_LAP(cls, 1)) for cls in flowers]

    for sets, actual in tests:
        i = 0
        for row in sets.iterrows():
            i += 1 if predict_class(row[1], flowers) == actual else 0
        print(f"{actual} percision = {round(100 * i / len(sets), 2)}%")


if __name__ == "__main__":
    main()
