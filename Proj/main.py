"""Main Module to run entire simulation"""

from numbers import Number
import os
import time

from pathos.pools import ProcessPool as Pool
from phe import EncryptedNumber, EncodedNumber
from phe import PaillierPrivateKey as PrivKey
from phe import PaillierPublicKey as PubKey
from server import Server
import dataset
import data_frames as FRAME
from user import User

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def test_run(eps: float, key: int):
    users: list[User] = dataset.get_dataset(True)  # Get all users as objects
    server = Server(users, epsilon=eps, key_size=key)  # Initialize a server

    # Example calculation given a list of attributes, determined upon request
    def test(pub: PubKey, acc: EncryptedNumber, usr: list[Number]) -> EncryptedNumber | bool:
        calories = usr[0]
        mod_active_dist = usr[1]

        if mod_active_dist != 0:  # Check for an actual value
            acc = acc + EncodedNumber.encode(pub, calories * mod_active_dist)
            return acc

        return False

    # Run function with the fields "Daily calories" and "Daily moderately active distance" for parameters
    request_ldp = 0

    for _ in range(10):
        request_ldp += server.requestAction([FRAME.DAILY.CALORIES, FRAME.DAILY.MODERATELY_ACTIVE_DISTANCE], 0, test).getAvg()

    request_ldp /= 10

    request_actual = server.requestAction([FRAME.DAILY.CALORIES, FRAME.DAILY.MODERATELY_ACTIVE_DISTANCE], 0, test, True).getAvg()

    return (eps, 100 * abs(request_actual - request_ldp) / request_actual)


def timedTest(eps: float, key: int):
    t0 = time.time()
    test_run(eps, key)
    t1 = time.time()
    return (key, t1 - t0)


def main():
    """Main Function"""
    dataset.get_dataset() # Cache dataset

    print("Running key variants")

    results = None
    with Pool(os.cpu_count()) as proc:
        results = proc.map(lambda key_size: timedTest(5, key_size), range(256, 4096, 64))

    print(results)

    x, values = zip(*results)

    plt.style.use("dark_background")
    fig, ax = plt.subplots()
    ax.set_xlabel("Key Size")
    ax.set_ylabel("Time (S)")
    ax.set_title("Calculation Time")
    plt.plot(x, values, "ro-")
    fig.savefig("report/img/time_plot.png")

    print("Running epsilon variants")

    results = None
    with Pool(os.cpu_count()) as proc:
        results = proc.map(lambda eps: test_run(eps / 100, 512), range(10, 1000, 5))

    print(results)

    x, values = zip(*results)

    plt.figure()
    plt.style.use("dark_background")
    fig, ax = plt.subplots()
    ax.set_xlabel("Epsilon")
    ax.set_ylabel("Error (%)")
    ax.set_title("Calculation Error")
    plt.plot(x, values, "ro-")
    fig.savefig("report/img/error_plot.png")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  # cd to where actual file is
    main()
