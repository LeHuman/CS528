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
    occupation: str
    race: Race

    # r_1, ..., r_m
    groupedOccupations: set

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

        self.occupation = occupation.strip()
        # self.groupedOccupations = set() if self.occupation == "?" else set([Occupation(self.occupation)])
        self._initSets()

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
        for occ in self.groupedOccupations:
            for _ in range(occ.count):
                fnl += f"{occ.value}, {self.age.getValue()}, {self.education.getValue()}, {self.marital_status.getValue()}, {self.race.getValue()}\n"
        return fnl.removesuffix("\n")

    def _privateStr(self) -> str:
        return f"\t{self.occupation}, {self.age.value}, {self.education.value}, {self.marital_status.value}, {self.race.value}\n"

    def privateStr(self) -> str:
        fnl = f"KMin: {self.k_min} {self.count}x\n"

        userSet = list(self.userSet)
        userSet.sort(key=lambda x: x.occupation)

        for usr in userSet:
            fnl += usr._privateStr()
        return fnl.removesuffix("\n")

    def __str__(self) -> str:
        fnl = f"KMin: {self.k_min} {self.count}x {self.age.getValue()}, {self.education.getValue()}, {self.marital_status.getValue()}, {self.race.getValue()}\n"
        for occ in self.groupedOccupations:
            fnl += f"\t{str(occ)}\n"
        return fnl

    def attributes(self) -> tuple:
        return (self.age, self.education, self.marital_status, self.race)

    def _initSets(self):
        self.groupedOccupations = set([Occupation(self.occupation)])
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

        # TODO: only extract outliers dependend on recursive cl diversity
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
                            if self.count > 1:
                                purged.add(user)
                                self.userSet.remove(user)
                                u = self.userSet.pop()
                                for user in self.userSet:
                                    u.add(user)
                                purged.add(u)
                            else:
                                purged.add(user)

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
        attrCount = 4
        for attr in self.attributes():
            div = attr.gen_max / attrCount + attr.ratio
            if div <= topRat:
                topRat = div
                topAttr = attr
        return topAttr

    def generalized(self) -> bool:
        for attr in self.attributes():
            if attr.gen_max != attr.gen_level:
                return False
        return True

    def kReached(self) -> bool:
        return self.count >= self.k_min

    def lReached(self) -> bool:
        if not self.l_min:
            return True
        return len(self.groupedOccupations) >= self.l_min

    def satisfied(self) -> bool:
        return self.kReached() and self.lReached()