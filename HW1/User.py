UID = 0


class User:
    UID = None
    k_min = 0

    age = None
    education = None
    marital_status = None
    occupation = None
    race = None

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
        self.age = age.strip()
        self.education = education.strip()
        self.marital_status = marital_status.strip()
        self.occupation = occupation.strip()
        self.race = race.strip()
        self.k_min = 10 if "<=50K" in salary else 5
        global UID
        self.UID = UID
        UID += 1

    def __str__(self) -> str:
        return f"ID:{self.UID}\tK:{self.k_min}\n\tage: {self.age}\n\teducation: {self.education}\n\tmarital_status: {self.marital_status}\n\toccupation: {self.occupation}\n\trace: {self.race}"