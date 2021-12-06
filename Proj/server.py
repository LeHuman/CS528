"""module containing server related things"""

from Pyfhel import Pyfhel, PyPtxt, PyCtxt
from user import User

class Server:
    """Server Class for database sim"""
    
    userAgg : User

    def __init__(self) -> None:
        userAgg = User(-1)
    
    def collectValue(self):
        pass
