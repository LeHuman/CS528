"""Module used for interpreting the user dataset"""

import os

import user, pickle
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
from pathos.pools import ProcessPool as Pool
from pathos.pools import ThreadPool as PyThreads
from user import User

PICKLE_PATH: str = "users.obj"


def __create_users(df: DataFrame) -> list[User]:
    users: list[User] = []

    for id in df["Id"].unique():
        df_usr = df[df["Id"] == id]
        usr = User(id)
        usr.data = df_usr
        users.append(usr)

    return users


def tick():
    print("|", end="", flush=True)


def parallel_apply(data, func, num_of_processes=12):
    data_split = np.array_split(data, num_of_processes)
    with Pool(num_of_processes) as p:
        return pd.concat(p.map(lambda chunk: chunk.apply(func), data_split))


def daily_frame() -> DataFrame:
    daily_df = pd.read_csv("dataset/dailyActivity_merged.csv")

    tick()
    daily_df["ActivityDate"] = parallel_apply(daily_df["ActivityDate"], lambda x: user.convert_dataset_date(x, True))

    tick()
    return daily_df


def heart_frame() -> DataFrame:
    heart_df = pd.read_csv("dataset/heartrate_seconds_merged.csv")

    tick()
    heart_df = heart_df.rename(columns={"Time": "ActivityDate"})
    heart_df["ActivityDate"] = parallel_apply(heart_df["ActivityDate"], lambda x: user.convert_dataset_date(x))

    tick()
    return heart_df


def sleep_frame() -> DataFrame:
    sleep_df = pd.read_csv("dataset/sleepDay_merged.csv")

    tick()
    sleep_df = sleep_df.rename(columns={"SleepDay": "ActivityDate"})
    sleep_df["ActivityDate"] = parallel_apply(sleep_df["ActivityDate"], lambda x: user.convert_dataset_date(x))

    tick()
    return sleep_df


def hourly_frame() -> DataFrame:
    hourly_cal: DataFrame = pd.read_csv("dataset/hourlyCalories_merged.csv")
    hourly_int: DataFrame = pd.read_csv("dataset/hourlyIntensities_merged.csv")
    hourly_stp: DataFrame = pd.read_csv("dataset/hourlySteps_merged.csv")

    tick()
    hourly_df = hourly_cal.merge(hourly_int, "left", ("Id", "ActivityHour")).merge(hourly_stp, "left", ("Id", "ActivityHour"))
    hourly_df = hourly_df.rename(columns={"ActivityHour": "ActivityDate"})

    tick()

    hourly_df["ActivityDate"] = parallel_apply(hourly_df["ActivityDate"], lambda x: user.convert_dataset_date(x))

    tick()
    return hourly_df


def __gen_users() -> list[User]:
    """Generates python object representation of dataset

    Returns:
        list[User]: List of users from the dataset
    """
    frames: list[DataFrame] = [daily_frame, heart_frame, sleep_frame, hourly_frame]

    # Concurrently interpret multiple CSVs
    with PyThreads(len(frames)) as pool:  # TODO: use actual multiprocessing
        frames = pool.map(lambda f: f(), frames)
        print()

    daily_df = frames[0]
    heart_df = frames[1]
    sleep_df = frames[2]
    hourly_df = frames[3]

    # Merge all datasets
    daily_df = (
        daily_df.merge(heart_df, "outer", ("Id", "ActivityDate"))
        .merge(sleep_df, "outer", ("Id", "ActivityDate"))
        .merge(hourly_df, "outer", ("Id", "ActivityDate"))
    )

    # Create Users given dataset
    users = __create_users(daily_df)

    with open(PICKLE_PATH, "w", encoding="utf-8") as file:
        pickle.dump(users, file.buffer)

    return users


def __get_pickled() -> list[User]:
    """Retrieves python object representation of dataset from local cache

    Returns:
        list[User]: List of users from the dataset
    """
    with open(PICKLE_PATH, "rb") as file:
        return pickle.load(file)


def get_dataset() -> list[User]:
    """Retrieves python object representation of dataset, if already made, else make it

    Returns:
        list[User]: List of users from the dataset
    """
    if os.path.exists(PICKLE_PATH):
        print("Using cached dataset")
        return __get_pickled()

    print("Generating user base")
    return __gen_users()


def main():
    """Main Function"""

    users: list[User] = get_dataset()

    for usr in users:
        print(usr)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  # cd to where actual file is
    main()
