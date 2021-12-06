"""Main Module to run entire simulation"""

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
    users: list[User] = dataset.get_dataset()
    server = Server(users, epsilon=2)

    for user in users:
        print(user)

    def test(acc: EncryptedNumber, usr: EncodedNumber) -> EncryptedNumber:
        acc = acc + math.sqrt(usr.decode())
        return acc

    print(server.requestFieldAvg(FRAME.HEART.BPM).value)
    print(server.requestAction(FRAME.DAILY.MODERATELY_ACTIVE_DISTANCE, 0, test).value)

    users[5]


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  # cd to where actual file is
    main()
