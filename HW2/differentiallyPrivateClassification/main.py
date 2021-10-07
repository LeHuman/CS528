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


def lapNoiseAVG(eps):
    sensitivity = 1 / eps
    return np.random.laplace(0, sensitivity, 1)[0]


def dpLAPData(eps: float, classData: DataFrame) -> DataFrame:
    df = DataFrame(data={"mean": classData.mean(), "std": classData.std()})
    df = df.applymap(lambda x: x + lapNoiseAVG(eps))
    return df


class Flower:
    df: DataFrame = None
    cls = ""
    n = 0

    def __init__(self, cls: str, n: int, classStats: DataFrame) -> None:
        self.cls = cls
        self.n = n
        self.df = classStats

    def gaussianProb(self, x: float) -> float:
        return norm.pdf(x, self.df["mean"], self.df["std"])


def dataStats(frame: DataFrame) -> DataFrame:
    cls = frame["class"].values[0]
    framed = frame.drop("class", axis=1)
    return DataFrame(data={"mean": framed.mean(), "std": framed.std(), "n": len(frame), "class": cls})


def gaussianProb(x: float, series: Series) -> float:
    return norm.pdf(x, series["mean"], series["std"])


def classProb(entry: Series, datasetStats: tuple[DataFrame]) -> dict[str, float]:
    n = int(sum(df["n"][0] for df in datasetStats))
    probabilities = dict()
    for stats in datasetStats:
        cls = stats["class"].values[0]
        probabilities[cls] = stats["n"].values[0] / n
        for i, stat in stats.iterrows():
            probabilities[cls] *= gaussianProb(entry[i], stat)
    return probabilities


def input2S(sepal_length, sepal_width, petal_length, petal_width) -> Series:
    return Series(data={"sepal-length": sepal_length, "sepal-width": sepal_width, "petal-length": petal_length, "petal-width": petal_width})


def predictClass(dimensions: tuple[float], datasetStats: tuple[DataFrame]) -> str:
    prob = classProb(input2S(*dimensions), datasetStats)
    return max(prob)


# Main Function
def main():
    print("\nDifferentially Private Classification\n")

    flowers = pd.read_csv("dataset/iris.data")

    setosas = flowers[flowers["class"] == "Iris-setosa"]
    versicolours = flowers[flowers["class"] == "Iris-versicolor"]
    virginicas = flowers[flowers["class"] == "Iris-virginica"]

    datasetStats = (dataStats(setosas), dataStats(versicolours), dataStats(virginicas))

    # print(dpLAPData(1, setosas))

    print(predictClass((5.7, 2.9, 4.2, 1.3), datasetStats))


if __name__ == "__main__":
    main()