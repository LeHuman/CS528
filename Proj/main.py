"""Main Module to run entire simulation"""

from numbers import Number
import os

import math
import phe as HE
from phe import EncryptedNumber, EncodedNumber
from phe import PaillierPrivateKey as PrivKey
from phe import PaillierPublicKey as PubKey
from server import Server
import dataset
import data_frames as FRAME
from user import User


def main():
    """Main Function"""
    users: list[User] = dataset.get_dataset()  # Get all users as objects
    server = Server(users, epsilon=5)  # Initialize a server with privacy parameter epsilon of 3

    # Example calculation given a list of attributes, determined upon request
    def test(pub: PubKey, acc: EncryptedNumber, usr: list[Number]) -> EncryptedNumber | bool:
        calories = usr[0]
        mod_active_dist = usr[1]

        if mod_active_dist != 0:
            acc = acc + EncodedNumber.encode(pub, calories * mod_active_dist)
            return acc

        return False

    print(server.requestFieldAvg(FRAME.HEART.BPM).value)  # Print the overall average of heart BPM

    # Run function test with the fields "daily calories" and "Daily moderately active distance"
    request = server.requestAction([FRAME.DAILY.CALORIES, FRAME.DAILY.MODERATELY_ACTIVE_DISTANCE], 0, test)
    print(request.value / request.counter)  # Print the average, counter is how many users actually ran the calculation


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  # cd to where actual file is
    main()
