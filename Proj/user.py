"""Module containing user related things"""

from numbers import Number
from typing import Callable

import diffprivlib
import phe as HE
from phe import EncryptedNumber, EncodedNumber
from phe import PaillierPrivateKey as PrivKey
from phe import PaillierPublicKey as PubKey
from pandas.core.series import Series
from data_frames import FRAME_ID, FRAME_TIME, FIELD
from pandas.core.frame import DataFrame


class UserRequest:
    id_num: int  # ID of the user giving data
    field: FIELD  # Field of this request
    time: float  # UNIX Timestamp
    value: Number  # The actual value being passed
    pub_key: PubKey = None

    def __init__(self, eps: float, id_num: int, field: FIELD, value: Number, time: float = -1, sensitivity=1) -> None:
        self.id_num = id_num
        self.field = field
        self.time = self.export_value(time, eps, sensitivity * 2) if time > 0 else None
        self.value = self.export_value(value, eps, sensitivity)

    def __str__(self) -> str:
        return f"ID:{self.id_num} FIELD:{self.field} TIME:{self.time} VALUE:{self.value}"

    def encode(self, key: PubKey):
        if self.pub_key == None:
            self.pub_key = key
            self.value = EncodedNumber.encode(key, self.value)
            if isinstance(self.time, Number):
                self.time = EncodedNumber.encode(key, self.time)
        else:
            raise Exception("UserRequest already encoded")

    def export_value(self, value: Number, eps: float, sensitivity) -> Number:
        """Return value with added laplace noise

        Args:
            value ([type]): Value to add noise to
            eps (float): Privacy parameter
            sensitivity (int, optional): Sensitivity parameter.

        Returns:
            Number: The noisy value
        """
        return self.field.TYPE(diffprivlib.mechanisms.Laplace(epsilon=eps, sensitivity=sensitivity).randomise(value))


class User:
    """User data class for fitbit data"""

    id_num: int
    data: dict[str, DataFrame]

    def __init__(self, id_num: int, data: dict[str, DataFrame]) -> None:
        self.id_num = id_num
        self.data = data

    def __hash__(self) -> int:
        return self.id_num

    def __str__(self) -> str:
        strs: list[str] = []

        for name, frame in self.data.items():
            strs.append(
                "\t{}\n\t\t{}".format(
                    name,
                    str(frame.drop(FRAME_TIME, axis=1).drop(FRAME_ID, axis=1).count())
                    .replace("dtype: int64", "")
                    .replace("\n", "\n\t\t")
                    .strip("\n\t")
                    + "\n",
                ).replace("\t", "  ")
            )

        return f"--------[ {self.id_num} ]--------\n{''.join(strs)}"

    def __get_field(self, field: FIELD, with_time=True) -> DataFrame | Series:
        cat = self.data[field.ENTRY]
        if with_time:
            return cat.loc[:, [FRAME_TIME, field]]
        else:
            return cat[field]

    def __get_field_avg(self, field: FIELD) -> Number:
        return self.__get_field(field, False).mean()

    def request_action(self, field: FIELD, eps: float, pub: PubKey, action: Callable[[EncodedNumber], None]) -> bool:
        try:
            ur = UserRequest(eps, self.id_num, field, self.__get_field_avg(field))
            ur.encode(pub)
            action(ur.value)
            return True
        except KeyError:  # Not all users have the same fields
            return False