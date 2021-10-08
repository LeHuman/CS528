# py 3.9.7

"""
    CS528 - Data Privacy and Security
    Illinois Institute of Technology
    Homework 2
    9-17-21

    hw2-3-classifier.py

    Differentially Private Classification using iris dataset
"""

import pandas as pd
import numpy as np
from scipy.stats import norm
from pandas.core.frame import DataFrame
from pandas.core.series import Series


class Flower:
    """Class representation of a flower type"""

    df: DataFrame = None
    cls = ""
    n = 0

    def __init__(self, cls: str, n: int, dataset: DataFrame) -> None:
        self.cls = cls
        self.n = n
        self.df = dataset.drop("class", axis=1)

    def __str__(self) -> str:
        return self.df.to_string()

    @staticmethod
    def noise_lap_avg(eps: float, n: int) -> float:
        """Generate laplacian noise fit for an average query

        Args:
            eps (float): Privacy parameter Epsilon
            n (int): Dataset size

        Returns:
            float: noise value
        """
        sensitivity = (1 / n) / eps
        return np.random.laplace(0, sensitivity, 1)[0]

    def dp_data_lap(self, eps: float) -> DataFrame:
        data = {
            "mean": self.df.mean() + self.noise_lap_avg(eps, len(self.df)),
            "std": self.df.std() + self.noise_lap_avg(eps, len(self.df)),
        }
        return DataFrame(data=data)

    def gaussian_prob(self, entry: Series, eps: float) -> float:
        """Get the Gaussian probability that an entry matches this class

        Args:
            entry (Series): The 1D Series of flower attributes

        Returns:
            float: Gaussian probability
        """

        df = self.dp_data_lap(eps)

        p = 1.0
        for i, stat in df.iterrows():
            p *= norm.pdf(entry[i], stat["mean"], stat["std"])
        return p


class Predictor:
    """Class used for predicting flower types while respecting a privacy budget"""

    flowers: list[Flower] = None
    eps = 0.0
    _eps = eps

    def __init__(self, flowers: list[Flower], eps: float = 0.0) -> None:
        self.flowers = flowers
        self.reset_budget(eps)

    def reset_budget(self, eps: float = None):
        """Resets the privacy budget

        Args:
            eps (float, optional): Privacy parameter Epsilon. Defaults to last value.
        """
        self._eps = eps or self._eps
        self.eps = self._eps

    def predict_class(self, entry: Series, eps: float = None) -> str:
        """Predict which class a 1D Series of flower attributes belongs to

        Args:
            entry (Series): The 1D Series of flower attributes

        Returns:
            str: The class name
        """

        assert self.eps != 0
        eps = self.eps if not eps else min(eps, self.eps)
        self.eps -= eps

        n = int(sum([f.n for f in self.flowers]))

        probabilities = dict()

        for flower in self.flowers:
            probabilities[flower.cls] = flower.gaussian_prob(entry, eps) * flower.n / n

        return max(probabilities.items(), key=lambda x: x[1])[0]


# Main Function
def main():
    print("\nDifferentially Private Classification\n")

    flowers_raw = pd.read_csv("dataset/iris.data")

    tests = (
        (flowers_raw[1:11].drop("class", axis=1), flowers_raw["class"][1]),
        (flowers_raw[51:61].drop("class", axis=1), flowers_raw["class"][51]),
        (flowers_raw[101:111].drop("class", axis=1), flowers_raw["class"][101]),
    )

    flowers = [
        flowers_raw[flowers_raw["class"] == "Iris-setosa"],
        flowers_raw[flowers_raw["class"] == "Iris-versicolor"],
        flowers_raw[flowers_raw["class"] == "Iris-virginica"],
    ]

    flowers = [Flower(cls["class"].values[0], len(cls), cls) for cls in flowers]

    predictor = Predictor(flowers)

    print("----[ Task 3(a-c) ]----\n")

    predictor.reset_budget(1)

    sample = flowers_raw.sample()
    actual = sample["class"].values[0]
    estimate = predictor.predict_class(sample)

    print(f"Actual: {actual}")
    print(f"Estimate: {estimate}")

    result = actual == estimate

    print("\n--[Remove entry from dataset]--\n")

    flowers_temp = flowers_raw.drop(flowers_raw.sample().index)
    flowers_temp = [
        flowers_raw[flowers_raw["class"] == "Iris-setosa"],
        flowers_raw[flowers_raw["class"] == "Iris-versicolor"],
        flowers_raw[flowers_raw["class"] == "Iris-virginica"],
    ]
    flowers_temp = [Flower(cls["class"].values[0], len(cls), cls) for cls in flowers_temp]
    flowers_temp = Predictor(flowers_temp, 1)

    estimate = flowers_temp.predict_class(sample)

    print(f"Actual: {actual}")
    print(f"Estimate: {estimate}")

    print(f"\nDo results match after removing user? {result == (actual == estimate)}")

    print("\n----[ Task 3(d) ]----")

    epsilons = (0.5, 1, 2, 4, 8, 16)

    for eps in epsilons:
        predictor.reset_budget(eps)
        queries = sum([len(s) for s, a in tests])
        print(f"\nepsilon : {eps} @ {queries} queries")
        eps /= queries
        for sets, actual in tests:
            i = 0
            for row in sets.iterrows():
                i += 1 if predictor.predict_class(row[1], eps) == actual else 0
            print(f"\t{actual} percision = {round(100 * i / len(sets), 2)}%")


if __name__ == "__main__":
    main()
