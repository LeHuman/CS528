# py 3.9.7

"""
    CS528 - Data Privacy and Security
    Illinois Institute of Technology
    Homework 2
    9-17-21
    
    main.py
    
    Differentially Private Classification using iris dataset
"""

import pandas as pd
import numpy as np

# Main Function
def main():
    print("\nDP - Differentially Private Classification")

    flowers = pd.read_csv("dataset/iris.data")
    print(flowers)


if __name__ == "__main__":
    main()