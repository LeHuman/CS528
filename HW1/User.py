from typing import Hashable
from Attr import Age, Attribute, Education, MaritalStatus, Race, Occupation

UID = 0


class User:
    UID = None
    k_min = 0
    l_min = None
    c_min = None
    count = 1

    age: Age
    education: Education
    marital_status: MaritalStatus
    _occupation: str
    race: Race

    # r_1, ..., r_m
    occupation: set

    # every User grouped under this user
    userSet: set

    def __init__(
        self,
        age,
        workclass,
        final_weight,
        education,
        education_num,
        marital_status,
        occupation,
        relationship,
        race,
        sex,
        capital_gain,
        capital_loss,
        hours_per_week,
        native_country,
        salary,
        k=None,
        l=None,
        c=None,
    ):

        self.age = Age(age.strip())
        self.education = Education(education.strip())
        self.marital_status = MaritalStatus(marital_status.strip())
        self.race = Race(race.strip())

        self._occupation = occupation.strip()
        self.occupation = set() if self._occupation == "?" else set([Occupation(self._occupation)])

        self.userSet = set([self])

        if k:
            self.k_min = k
        else:
            self.k_min = 10 if "<=50K" in salary.strip() else 5  # set user preference

        # No user preference for these values
        self.l_min = l if l else None
        self.c_min = c if c else None

        global UID
        self.UID = UID
        UID += 1

    def __eq__(self, o: object) -> bool:  # check equivalence only with other User types
        return (
            o
            and self.k_min == o.k_min
            and self.age == o.age
            and self.education == o.education
            and self.marital_status == o.marital_status
            and self.race == o.race
        )

    def __hash__(self) -> int:
        return id(self)

    def basicStr(self) -> str:
        fnl = ""
        for occ in self.occupation:
            for _ in range(occ.count):
                fnl += f"{occ.value}, {self.age.getValue()}, {self.education.getValue()}, {self.marital_status.getValue()}, {self.race.getValue()}\n"
        return fnl.removesuffix("\n")

    def _privateStr(self) -> str:
        return f"\t{self._occupation}, {self.age.value}, {self.education.value}, {self.marital_status.value}, {self.race.value}\n"

    def privateStr(self) -> str:
        fnl = f"KMin: {self.k_min} {self.count}x\n"

        userSet = list(self.userSet)
        userSet.sort(key=lambda x: x._occupation)

        for usr in userSet:
            fnl += usr._privateStr()
        return fnl.removesuffix("\n")

    def __str__(self) -> str:
        fnl = f"KMin: {self.k_min} {self.count}x {self.age.getValue()}, {self.education.getValue()}, {self.marital_status.getValue()}, {self.race.getValue()}\n"
        for occ in self.occupation:
            fnl += f"\t{str(occ)}\n"
        return fnl

    def attributes(self) -> tuple:
        return (self.age, self.education, self.marital_status, self.race)

    def add(self, user) -> bool:
        if self == user:
            self.count += user.count
            self.occupation = self.occupation.union(user.occupation)
            self.userSet = self.userSet.union(user.userSet)
            return True
        return False

    def diverseAttr(self) -> Attribute:
        topRat = 21
        topAttr = None
        for attr in self.attributes():
            if attr.gen_max / 4 + attr.ratio <= topRat:
                topRat = attr.ratio
                topAttr = attr
        return topAttr

    def kReached(self) -> bool:
        return self.count >= self.k_min

    def lReached(self) -> bool:
        if not self.l_min:
            return True
        return len(self.occupation) >= self.l_min

    def satisfied(self) -> bool:
        return self.kReached() and self.lReached()