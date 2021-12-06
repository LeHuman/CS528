"""Main Module to run entire simulation"""

import os

import server, dataset
from user import User


def main():
    """Main Function"""
    users: list[User] = dataset.get_dataset()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  # cd to where actual file is
    main()
