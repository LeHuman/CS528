from Attr import Age, Education, MaritalStatus, Race

UID = 0


class User:
    UID = None
    k_min = 0

    age: Age
    education: Education
    marital_status: MaritalStatus
    race: Race

    occupation: str

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

        self.occupation = None if occupation.strip() == "?" else occupation.strip()
        self.k_min = 10 if "<=50K" in salary.strip() else 5

        global UID
        self.UID = UID
        UID += 1

    def __str__(self) -> str:
        return f"ID:{self.UID}\tK:{self.k_min}\n\toccupation: {self.occupation}\n\tage: {self.age.getValue()}\n\teducation: {self.education.getValue()}\n\tmarital_status: {self.marital_status.getValue()}\n\trace: {self.race.getValue()}"

    def attributes(self) -> tuple:
        return (self.age, self.education, self.marital_status, self.race)