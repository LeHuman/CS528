"""module containing user related things"""

import datetime, diffprivlib
import time
import pandas as pd
from pandas.core.frame import DataFrame
from numbers import Number


def convert_dataset_date(date: str, short: bool = False) -> float:
    """Create a datetime object from a dataset date

    Args:
        date (str): date str from the dataset

    Returns:
        float: UNIX Timestamp representing the date str
    """

    return time.mktime(datetime.datetime.strptime(date, "%m/%d/%Y" if short else "%m/%d/%Y %I:%M:%S %p").timetuple())


class User:
    """User data class for fitbit data"""

    id_num: int
    data: DataFrame

    def __init__(self, id_num: int) -> None:
        self.id_num = id_num
        self.data = DataFrame()

    def __hash__(self) -> int:
        return self.id_num

    def __str__(self) -> str:
        return "--------[ {} ]--------\n{}".format(self.id_num, str(self.data.rename(columns={"Id": "Total Entries"}).count()))

    def export_value(self, value, eps: float) -> Number:
        """Return value with added laplace noise

        Args:
            value ([type]): Value to add noise to
            eps (float): Privacy parameter

        Returns:
            Number: The noisy value
        """
        return value.__class__(diffprivlib.mechanisms.Laplace(epsilon=eps, sensitivity=0.5).randomise(value))

    # def add_data(self, df: DataFrame) -> None:
    #     """Add user data to this User

    #     Args:
    #         df (DataFrame): The data frame containing the entries to add
    #     """
    #     self.data.append(df)
