# py 3.9.6

"""
    CS528 - Data Privacy and Security
    Illinois Institute of Technology
    Homework 1
    9-17-21
    
    User.py
    
    User class is used to help abstract each "user"; aka each line in the data set, into a usable object

    Users can be grouped up with other users. When this happens, their occupations are also kept track of
    separately using a Counter object.
"""
from math import log
from typing import Counter
from Attr import TOTAL_ATTRIBUTES, Age, Attribute, Education, MaritalStatus, Race


UID = 0  # Counter for UIDs


class User:
    UID = None  # Used for ease of hash func and general ID of each user
    k_min = 0  # The minimum k-anonymity requested by the user
    l_min = None  # The minimum entropy l-diversity requested by the user
    c_min = None  # The minimum recursive c l-diversity requested by the user
    count = 1  # The number of users grouped with this user, aka a q*-block

    # Each attribute is casted into a class where generalizations must be made
    age: Age
    education: Education
    marital_status: MaritalStatus
    occupation: str
    race: Race

    # r_1, ..., r_m
    # Counter for each occupation that is grouped with this User / q*-block
    groupedOccupations: Counter[str] = None

    # Every User grouped under this User
    userSet: set = None

    def __init__(  # Include all attributes, just to make it cleaner when splitting the data lines
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

        # "Cast" each string into an object
        self.age = Age(age.strip())
        self.education = Education(education.strip())
        self.marital_status = MaritalStatus(marital_status.strip())
        self.race = Race(race.strip())
        self.occupation = occupation.strip()

        # initialize each set; user set and occupation set
        self._initSets()

        if k:
            self.k_min = k  # set k if default is given
        else:
            self.k_min = 10 if "<=50K" in salary.strip() else 5  # else, set by user preference

        # No user preference for these values
        self.l_min = l if l else None
        self.c_min = c if c else None

        # Set unique UserID
        global UID
        self.UID = UID
        UID += 1

    # Check equivalence only with other User types, does not check isinstance
    def __eq__(self, o: object) -> bool:
        return (
            o
            and self.k_min == o.k_min  # NOTE: Users are matched if they have then same k_min, k=5 or k=10 in our case
            and self.age == o.age
            and self.education == o.education
            and self.marital_status == o.marital_status
            and self.race == o.race
        )

    # Hash func for sets
    def __hash__(self) -> int:
        return UID

    # See toStr
    def __str__(self) -> str:
        return self.toStr()

    # Return the most basic representation of this User / q*-block
    def basicStr(self) -> str:
        fnl = ""
        for occ, c in self.groupedOccupations.items():
            for _ in range(c):
                fnl += (
                    f"{occ}, {self.age.getValue()}, {self.education.getValue()}, {self.marital_status.getValue()}, {self.race.getValue()}\n"
                )
        return fnl.removesuffix("\n")

    # Return the un-anonymized representation of this User, used internally
    def _privateStr(self) -> str:
        return f"\t{self.occupation}, {self.age.value}, {self.education.value}, {self.marital_status.value}, {self.race.value}\n"

    # Return the un-anonymized representation of this User / q*-block, used for post anon comparison
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

    # Return a condensed representation of this q*-block
    def toStr(self) -> str:
        fnl = f"{self.count}x | KMin: {self.k_min}, D:{round(self.getDistortion(),4)}, P:{round(self.getPrecision(),4)}\n  Attrs: {self.age.getValue()}, {self.education.getValue()}, {self.marital_status.getValue()}, {self.race.getValue()}\n"
        for occ, c in self.groupedOccupations.items():
            fnl += f"\t{c}x {occ}\n"
        return fnl.removesuffix("\n")

    # Return the attributes for this User
    def attributes(self) -> tuple[Attribute]:
        return (self.age, self.education, self.marital_status, self.race)

    # Initialize or reinitialize this User's sets if they are not empty
    def _initSets(self):
        if not self.userSet or self.count != 1:
            self.groupedOccupations = Counter({self.occupation: 1})
            self.userSet = set([self])
            self.count = 1

    # Add a user to this User / q*-block if it is equivalent
    def add(self, user) -> bool:
        if self == user:
            self.count += user.count
            self.groupedOccupations.update(user.groupedOccupations)
            self.userSet = self.userSet.union(user.userSet)
            user._initSets()  # re-init the user's sets that is being merged
            return True
        return False

    # Return the attribute that has the least distortion
    def diverseAttr(self) -> Attribute:
        topRat = 21
        topAttr = None
        for attr in self.attributes():
            if attr.distortion <= topRat:
                topRat = attr.distortion
                topAttr = attr
        return topAttr

    # Whether this user / q*-block has been completely generalized, rendering it useless
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

    # Whether k-anonymization critera has been satisfied
    def kReached(self) -> bool:
        return self.count >= self.k_min  # check if at least k_min users are in this q*-block

    # Part of entropy l-diversity equation, mostly for better understanding
    def p_qSTARs(self, SACount: int) -> float:  # p(q*,s)
        return SACount / self.count

    # Whether entropy l-diversity critera has been satisfied
    def lReached(self) -> bool:
        if not self.l_min or self.c_min:  # Ignore entropy l diversity check when c is set, this means we are using c-l diversity
            return True

        s = 0

        # Run the sum of the occupation counts
        for _, c in self.groupedOccupations.items():
            s += self.p_qSTARs(c) * log(self.p_qSTARs(c))  # What is s'?

        # Check that there are l_min unique SAs, and the side effect of at least l distinct SAs
        return -s >= log(self.l_min) and len(self.groupedOccupations) >= self.l_min

    # Whether c-l diversity critera has been satisfied
    def cReached(self) -> bool:
        if not self.c_min or not self.l_min:  # We need both l and c for c-l diversity
            return True

        # We only care about the number for each occupation
        uniqueOccupationCounts = list(self.groupedOccupations.values())

        # There are not enough users to satisfy this l value
        if len(uniqueOccupationCounts) < self.l_min:
            return False

        # get the occupation with highest count
        vH = max(uniqueOccupationCounts)

        # remove r_1
        uniqueOccupationCounts.remove(max(uniqueOccupationCounts))

        # remove l - 1 possible values of S
        for _ in range(1, self.l_min - 1, 1):
            uniqueOccupationCounts.remove(min(uniqueOccupationCounts))

        return vH < self.c_min * (sum(uniqueOccupationCounts))  # r_1 < c * sum(r_l, ..., r_m)

    # Whether this user / q*-block k-anonymization, l-diversity, or recursive c-l diversity critera has been satisfied
    def satisfied(self) -> bool:
        return self.kReached() and self.lReached() and self.cReached()
