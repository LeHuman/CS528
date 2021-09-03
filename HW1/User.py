UID = 0

class User:
    UID = None
    age = None
    workclass = None
    final_weight = None
    education = None
    education_num = None
    marital_status = None
    occupation = None
    relationship = None
    race = None
    sex = None
    capital_gain = None
    capital_loss = None
    hours_per_week = None
    native_country = None
    salary = None

    def __init__(self,
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
salary
):
        self.age = age.strip()
        self.workclass = workclass.strip()
        self.final_weight = final_weight.strip()
        self.education = education.strip()
        self.education_num = education_num.strip()
        self.marital_status = marital_status.strip()
        self.occupation = occupation.strip()
        self.relationship = relationship.strip()
        self.race = race.strip()
        self.sex = sex.strip()
        self.capital_gain = capital_gain.strip()
        self.capital_loss = capital_loss.strip()
        self.hours_per_week = hours_per_week.strip()
        self.native_country = native_country.strip()
        self.salary = salary.strip()
        global UID
        self.UID = UID
        UID += 1

    def __str__(self) -> str:
        return f"{self.UID}\n\t{self.age}\n\t{self.workclass}\n\t{self.final_weight}\n\t{self.education}\n\t{self.education_num}\n\t{self.marital_status}\n\t{self.occupation}\n\t{self.relationship}\n\t{self.race}\n\t{self.sex}\n\t{self.capital_gain}\n\t{self.capital_loss}\n\t{self.hours_per_week}\n\t{self.native_country}\n\t{self.salary}"