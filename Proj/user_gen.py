import os

import user, pickle
from typing import Type
import pandas as pd
from pandas.core.frame import DataFrame
from user import User

PICKLE_PATH: str = "users.obj"


def add_entries(user_map: dict[int, User], cType: Type, df: DataFrame):
    for ent in df.iterrows():
        usr: User
        ent = ent[1]
        id_n = ent["Id"]

        if not (usr := user_map.get(id_n)):
            user_map[id_n] = User(id_n)
            usr = user_map[id_n]

        ent = cType(*ent.values[1:])
        usr.add_entry(ent)


def gen_users() -> list[User]:
    """Generates python object representation of dataset

    Returns:
        list[User]: List of users from the dataset
    """
    user_map: dict[int, User] = dict()

    daily_df = pd.read_csv("dataset/dailyActivity_merged.csv")
    heart_df = pd.read_csv("dataset/heartrate_seconds_merged.csv")
    sleep_df = pd.read_csv("dataset/sleepDay_merged.csv")

    hourly_cal: DataFrame = pd.read_csv("dataset/hourlyCalories_merged.csv")
    hourly_int: DataFrame = pd.read_csv("dataset/hourlyIntensities_merged.csv")
    hourly_stp: DataFrame = pd.read_csv("dataset/hourlySteps_merged.csv")
    hourly_df = hourly_cal.merge(hourly_int, "left", ("Id", "ActivityHour")).merge(hourly_stp, "left", ("Id", "ActivityHour"))

    add_entries(user_map, user.DailyActivity, daily_df)
    add_entries(user_map, user.HourlyActivity, hourly_df)
    add_entries(user_map, user.SleepTime, sleep_df)
    add_entries(user_map, user.HeartRate, heart_df)

    user_map = list(user_map.values())

    with open(PICKLE_PATH, "w", encoding="utf-8") as file:
        pickle.dump(user_map, file.buffer)

    return user_map


def get_pickled() -> list[User]:
    """Retrieves python object representation of dataset from local cache

    Returns:
        list[User]: List of users from the dataset
    """
    with open(PICKLE_PATH, "rb") as file:
        return pickle.load(file)


def get_user_list() -> list[User]:
    """Retrieves python object representation of dataset, if already made, else make it

    Returns:
        list[User]: List of users from the dataset
    """
    if os.path.exists(PICKLE_PATH):
        print("Using cached dataset")
        return get_pickled()

    print("Generating user base")
    return gen_users()


def main():
    """Main Function"""

    users: list[User] = get_user_list()

    for usr in users:
        print(usr)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  # cd to where actual file is
    main()
