"""Module used for interpreting the user dataset"""

import os

import pickle
import pandas as pd
from pandas.core.frame import DataFrame
from pathos.pools import ThreadPool as PyThreads

import data_frames as FRAME
from data_frames import FRAME_ID, FRAME_TIME
from user import User

PICKLE_PATH: str = "users.obj"


def create_users(dataframes: dict[str, DataFrame]) -> list[User]:
    user_map: dict[int, dict[str, DataFrame]] = dict()

    for df_name, df in dataframes.items():
        for id_num in df[FRAME_ID].unique():
            df_usr = df[df[FRAME_ID] == id_num]

            user_ent: dict[str, DataFrame]
            if not (user_ent := user_map.get(id_num)):
                user_map[id_num] = dict()
                user_ent = user_map[id_num]

            user_ent[df_name] = df_usr

    users: list[User] = []

    for id_num, data in user_map.items():
        users.append(User(id_num, data))

    return users


def gen_users() -> list[User]:
    """Generates python object representation of dataset

    Returns:
        list[User]: List of users from the dataset
    """

    names: list[str] = [
        FRAME.DAILY.VALUE,
        FRAME.HEART.VALUE,
        FRAME.SLEEP.VALUE,
        FRAME.HOURLY.VALUE,
    ]
    frames: list[DataFrame] = [FRAME.daily_frame, FRAME.heart_frame, FRAME.sleep_frame, FRAME.hourly_frame]

    # Concurrently interpret multiple CSVs
    with PyThreads(len(frames)) as pool:  # TODO: use actual multiprocessing
        frames = pool.map(lambda f: f(), frames)
        print()

    # Create Users given dataset
    users = create_users(dict(zip(names, frames)))

    with open(PICKLE_PATH, "w", encoding="utf-8") as file:
        pickle.dump(users, file.buffer)

    return users


def get_pickled() -> list[User]:
    """Retrieves python object representation of dataset from local cache

    Returns:
        list[User]: List of users from the dataset
    """
    with open(PICKLE_PATH, "rb") as file:
        return pickle.load(file)


def get_dataset(silent=False) -> list[User]:
    """Retrieves python object representation of dataset, if already made, else make it

    Returns:
        list[User]: List of users from the dataset
    """
    if os.path.exists(PICKLE_PATH):
        if not silent:
            print("Using cached dataset")
        return get_pickled()
    if not silent:
        print("Generating user base")
    return gen_users()


def main():
    """Main Function"""

    users: list[User] = get_dataset()

    for usr in users:
        print(usr)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  # cd to where actual file is
    main()
