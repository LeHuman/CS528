class Attribute:
    gen_max = 0
    gen_level = 0
    value = "*"

    def __init__(self, gen_max: int, value):
        self.gen_max = gen_max
        self.value = value

    def setGenLevel(self, gen: int):
        self.gen_level = max(0, min(gen, self.gen_max))

    def upGenLevel(self) -> int:
        if self.gen_max > self.gen_level:
            self.gen_level += 1
        return self.gen_level

    def downGenLevel(self) -> int:
        if self.gen_level > 0:
            self.gen_level -= 1
        return self.gen_level

    def getValue(self) -> str:
        return self.value


class Age(Attribute):
    def __init__(self, age: str):
        super().__init__(3, int(age))

    def getValue(self) -> str:
        if self.gen_level == 0:
            return str(self.value)
        elif self.gen_level == 1:
            if self.value < 30:
                return "<30"
            elif self.value >= 60:
                return ">=60"
            else:
                return f"{int(self.value / 10)}*"
        elif self.gen_level == 2:
            if self.value < 40:
                return "<40"
            else:
                return ">=40"
        else:
            return "*"


class Education(Attribute):

    values = {
        "higher": {
            "tertiary_education": (
                "Doctorate",
                "Assoc-voc",
                "Assoc-acdm",
                "Masters",
                "Bachelors",
                "Prof-school",
                "Some-college",
            ),
            "high_school": (
                "HS-grad",
                "12th",
                "11th",
                "10th",
            ),
        },
        "lower": {
            "middle_school": (
                "9th",
                "7th-8th",
            ),
            "elementry": (
                "5th-6th",
                "1st-4th",
                "Preschool",
            ),
        },
    }

    def __init__(self, education: str):
        super().__init__(3, education)

    def getValue(self) -> str:
        if self.gen_level == 0:
            return self.value
        elif self.gen_level == 1:
            for _, v in self.values.items():
                for _k, _v in v.items():
                    if self.value in _v:
                        return _k
        elif self.gen_level == 2:
            for k, v in self.values.items():
                for _k, _v in v.items():
                    if self.value in _v:
                        return k
        else:
            return "*"


class MaritalStatus(Attribute):

    values = {
        "married": (
            "Married-AF-spouse",
            "Married-civ-spouse",
            "Married-spouse-absent",
            "Separated",
        ),
        "not_married": (
            "Widowed",
            "Divorced",
            "Never-married",
        ),
    }

    def __init__(self, status: str):
        super().__init__(2, status)

    def getValue(self) -> str:
        if self.gen_level == 0:
            return self.value
        elif self.gen_level == 1:
            for k, v in self.values.items():
                if self.value in v:
                    return k
        else:
            return "*"


class Race(Attribute):

    values = {
        "white": ("White"),
        "nonWhite": (
            "Black",
            "Asian-Pac-Islander",
            "Amer-Indian-Eskimo",
            "Other",
        ),
    }

    def __init__(self, race: str):
        super().__init__(2, race)

    def getValue(self) -> str:
        if self.gen_level == 0:
            return self.value
        elif self.gen_level == 1:
            for k, v in self.values.items():
                if self.value in v:
                    return k
        else:
            return "*"