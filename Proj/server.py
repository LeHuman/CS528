"""module containing server related things"""

from numbers import Number
from typing import Callable
import phe as HE
from phe import EncryptedNumber
from phe import PaillierPrivateKey as PrivKey
from phe import PaillierPublicKey as PubKey
from pandas.core.frame import DataFrame
from phe.encoding import EncodedNumber
from user import User
import data_frames as FRAME
from data_frames import FIELD

KEY_SIZE = 1024


class ServerRequest:
    counter: int  # Number of users that worked on this request
    epsilon: float  # privacy value
    field: FIELD  # Field of this request
    value: EncryptedNumber  # The actual value being passed
    pub_key: PubKey  # PubKey used in this request
    action: Callable[[EncryptedNumber, EncodedNumber], EncryptedNumber]  # The function to run on the values

    def __init__(
        self,
        field: FIELD,
        value: Number,
        pub_key: PubKey,
        epsilon: float,
        action: Callable[[EncryptedNumber, EncodedNumber], EncryptedNumber],
    ) -> None:
        self.counter = 0
        self.epsilon = epsilon
        self.field = field
        self.value = pub_key.encrypt(value)
        self.pub_key = pub_key
        self.action = action

    def run(self, number: EncodedNumber):
        if self.action != None:
            self.value = self.action(self.value, number)

    def decrypt(self, priv_key: PrivKey) -> None:
        self.value = self.field.TYPE(priv_key.decrypt(self.value))

    def count(self, b: bool = True) -> None:
        if b:
            self.counter += 1

    def setAvg(self, priv_key: PrivKey) -> None:
        self.decrypt(priv_key)
        self.value /= self.counter


class Server:
    """Server Class for database sim"""

    __userAgg: User
    pub_key: PubKey
    __priv_key: PrivKey
    epsilon: float
    users: list[User]

    def __init__(self, users: list[User], epsilon: float = 3) -> None:
        self.__userAgg = User(
            -1,
            {
                FRAME.DAILY: DataFrame(),
                FRAME.HEART: DataFrame(),
                FRAME.SLEEP: DataFrame(),
                FRAME.HOURLY: DataFrame(),
            },
        )
        self.epsilon = epsilon
        self.users = users
        self.pub_key, self.__priv_key = HE.generate_paillier_keypair(n_length=KEY_SIZE)

    def getPubKey(self) -> PubKey:
        return self.pub_key

    def requestFieldAvg(self, field: FIELD) -> ServerRequest:
        request = ServerRequest(field, 0, self.pub_key, self.epsilon, lambda a, u: a + u)
        for user in self.users:
            request.count(user.request_action(field, request.epsilon, request.pub_key, request.run))
        request.setAvg(self.__priv_key)
        return request

    def requestAction(
        self, field: FIELD, init_value: Number, action: Callable[[EncryptedNumber, EncodedNumber], EncryptedNumber]
    ) -> ServerRequest:
        request = ServerRequest(field, init_value, self.pub_key, self.epsilon, action)
        for user in self.users:
            if user.request_action(field, request.epsilon, request.pub_key, request.run):
                request.counter += 1
        request.decrypt(self.__priv_key)
        return request

    # def requestComparison(self):
        

    def collectRequest(self, request: ServerRequest) -> None:
        field = request.field
        cat = self.__userAgg.data[field.ENTRY]
        cat[field] = request.value
        print(self.__userAgg)
