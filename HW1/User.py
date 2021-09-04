from Attr import Age, Attribute, Education, MaritalStatus, Race, Occupation

UID = 0


class User:
    UID = None
    k_min = 0
    count = 1

    age: Age
    education: Education
    marital_status: MaritalStatus
    race: Race

    occupation: set

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
    ):

        self.age = Age(age.strip())
        self.education = Education(education.strip())
        self.marital_status = MaritalStatus(marital_status.strip())
        self.race = Race(race.strip())

        self.occupation = set() if occupation.strip() == "?" else set([Occupation(occupation.strip())])
        self.k_min = 10 if "<=50K" in salary.strip() else 5

        global UID
        self.UID = UID
        UID += 1

    def __eq__(self, o: object) -> bool:
        return (
            o
            and self.k_min == o.k_min
            and self.age == o.age
            and self.education == o.education
            and self.marital_status == o.marital_status
            and self.race == o.race
        )

    def basicStr(self) -> str:
        fnl = ""
        for occ in self.occupation:
            for _ in range(occ.count):
                fnl += f"{occ.value}, {self.age.getValue()}, {self.education.getValue()}, {self.marital_status.getValue()}, {self.race.getValue()}\n"
        return fnl.removesuffix("\n")

    def __str__(self) -> str:
        fnl = f"{self.count}x {self.age.getValue()}, {self.education.getValue()}, {self.marital_status.getValue()}, {self.race.getValue()}\n"
        for occ in self.occupation:
            fnl += f"\t{str(occ)}\n"
        return fnl

    def attributes(self) -> tuple:
        return (self.age, self.education, self.marital_status, self.race)

    def add(self, user) -> bool:
        if self == user:
            self.count += user.count
            self.occupation = self.occupation.union(user.occupation)
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