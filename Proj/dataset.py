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


# def minMax(x):
#     return pd.Series(index=["min", "max"], data=[x.min(), x.max()])


def create_users(dataframes: dict[str, DataFrame]) -> list[User]:
    user_map: dict[int, dict[str, DataFrame]] = dict()

    for df_name, df in dataframes.items():
        for id in df[FRAME_ID].unique():
            df_usr = df[df[FRAME_ID] == id]

            user_ent: dict[str, DataFrame]
            if not (user_ent := user_map.get(id)):
                user_map[id] = dict()
                user_ent = user_map[id]

            user_ent[df_name] = df_usr

    users: list[User] = []

    for id, data in user_map.items():
        users.append(User(id, data))

    return users


def gen_users() -> list[User]:
    """Generates python object representation of dataset

    Returns:
        list[User]: List of users from the dataset
    """

    names: list[str] = [
        FRAME.DAILY,
        FRAME.HEART,
        FRAME.SLEEP,
        FRAME.HOURLY,
    ]
    frames: list[DataFrame] = [FRAME.daily_frame, FRAME.heart_frame, FRAME.sleep_frame, FRAME.hourly_frame]

    # Concurrently interpret multiple CSVs
    with PyThreads(len(frames)) as pool:  # TODO: use actual multiprocessing
        frames = pool.map(lambda f: f(), frames)
        print()

    # stat = ""

    # for df_name, df in zip(names, frames):
    #     stat += f"\n---< {df_name} >---\n{str(df.drop(FRAME_TIME, axis=1).drop(FRAME_ID, axis=1).apply(minMax))}"

    # print(stat)

    # Create Users given dataset
    users = create_users(dict(zip(names, frames)))

    # with open(PICKLE_PATH, "w", encoding="utf-8") as file:
    #     pickle.dump(users, file.buffer)

    return users


def get_pickled() -> list[User]:
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
        return get_pickled()

    print("Generating user base")
    return gen_users()


def main():
    """Main Function"""

    users: list[User] = get_dataset()

    # for usr in users:
    #     print(usr)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  # cd to where actual file is
    main()
