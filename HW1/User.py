from Attr import TOTAL_ATTRIBUTES, Age, Attribute, Education, MaritalStatus, Race, Occupation

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
    occupation: str
    race: Race

    # r_1, ..., r_m
    groupedOccupations: set = None

    # every User grouped under this user
    userSet: set = None

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
        self.occupation = Occupation(occupation.strip())

        self._initSets()

        if k:
            self.k_min = k  # set k if default is set
        else:
            self.k_min = 10 if "<=50K" in salary.strip() else 5  # else, set user preference

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
        for occ in self.groupedOccupations:
            for _ in range(occ.count):
                fnl += f"{occ.value}, {self.age.getValue()}, {self.education.getValue()}, {self.marital_status.getValue()}, {self.race.getValue()}\n"
        return fnl.removesuffix("\n")

    def _privateStr(self) -> str:
        return f"\t{self.occupation}, {self.age.value}, {self.education.value}, {self.marital_status.value}, {self.race.value}\n"

    def privateStr(self, basic=False) -> str:
        fnl = (
            f"{self.count}x | KMin: {self.k_min}, D:{round(self.getDistortion(),4)}, P:{round(self.getPrecision(),4)}\n"
            if not basic
            else ""
        )

        userSet = list(self.userSet)
        userSet.sort(key=lambda x: x.occupation)

        for usr in userSet:
            fnl += usr._privateStr()
        return fnl.removesuffix("\n")

    def toStr(self) -> str:
        fnl = f"{self.count}x | KMin: {self.k_min}, D:{round(self.getDistortion(),4)}, P:{round(self.getPrecision(),4)}\n  Attrs: {self.age.getValue()}, {self.education.getValue()}, {self.marital_status.getValue()}, {self.race.getValue()}\n"
        for occ in self.groupedOccupations:
            fnl += f"\t{str(occ)}\n"
        return fnl.removesuffix("\n")

    def __str__(self) -> str:
        return self.toStr()

    def attributes(self) -> tuple[Attribute]:
        return (self.age, self.education, self.marital_status, self.race)

    # Reset users that are the head of a group
    def _initSets(self):
        if not self.userSet or self.count != 1:
            self.groupedOccupations = set([self.occupation])
            self.userSet = set([self])
            self.count = 1

    def add(self, user) -> bool:
        if self == user:
            self.count += user.count
            self.groupedOccupations = self.groupedOccupations.union(user.groupedOccupations)
            self.userSet = self.userSet.union(user.userSet)
            user._initSets()  # re-init the user's sets that is being merged
            return True
        return False

    def extractOutliers(self) -> set:
        ocCount = dict()
        purged = set()

        # TODO: only extract outliers depending on recursive cl diversity

        if not self.c_min:
            return purged

        l = list(self.userSet)  # used to remove from global set while iterating

        for user in l:
            if not ocCount.get(user.occupation):
                ocCount[user.occupation] = 0
            ocCount[user.occupation] += 1

        for k, v in ocCount.items():
            if v == 1:
                self.groupedOccupations.remove(k)
                for user in l:
                    if user.occupation == k:
                        if user is self:
                            purged.union(self.userSet)

                            self._initSets()
                            return purged
                        else:
                            purged.add(user)
                            self.userSet.remove(user)
                            self.count -= 1

        return purged

    def diverseAttr(self) -> Attribute:
        topRat = 21
        topAttr = None
        for attr in self.attributes():
            if attr.distortion <= topRat:
                topRat = attr.distortion
                topAttr = attr
        return topAttr

    def generalized(self) -> bool:
        for attr in self.attributes():
            if attr.gen_level != attr.gen_max:
                return False
        return True

    # Get attribute distortion for this user / q*-block
    def getDistortion(self) -> float:
        d = 0
        for a in self.attributes():
            d += a.distortion
        return d

    # Get precision numerator of these users to calc table precision
    def getPrecisionNumerator(self) -> int:
        p = 0
        for a in self.attributes():
            p += a.precision_num
        return p * self.count

    # Get attribute precision for this user / q*-block
    def getPrecision(self) -> float:
        p = 0
        for a in self.attributes():
            p += a.precision_num
        return 1 - (p / TOTAL_ATTRIBUTES)

    def kReached(self) -> bool:
        return self.count >= self.k_min

    def lReached(self) -> bool:
        if not self.l_min:
            return True
        return len(self.groupedOccupations) >= self.l_min

    def satisfied(self) -> bool:
        return self.kReached() and self.lReached()