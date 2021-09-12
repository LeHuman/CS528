TOTAL_ATTRIBUTES = 4


class Attribute:
    gen_level = 0
    gen_max = 0
    distortion: float = 0.0
    precision_num: float = 0.0
    value = "*"
    gen_value = "*"

    def __init__(self, gen_max: int, value):
        self.gen_max = gen_max
        self.value = value
        self._setQualifiers()

    def __eq__(self, o: object) -> bool:  # IMPROVE: give each hierarchy value an id versus comparing strings
        return self.gen_value == o.gen_value

    def _setQualifiers(self):
        self.distortion = (self.gen_level / self.gen_max) / TOTAL_ATTRIBUTES
        self.precision_num = self.gen_level / self.gen_max  # h / |DGH_Ai|
        self.gen_value = self._getValue()

    def setGenLevel(self, gen: int):
        self.gen_level = max(0, min(gen, self.gen_max))
        self._setQualifiers()

    def upGenLevel(self):
        self.setGenLevel(self.gen_level + 1)

    def downGenLevel(self):
        self.setGenLevel(self.gen_level - 1)

    def _getValue(self) -> str:
        return self.value

    def getValue(self) -> str:
        return self.gen_value


class Age(Attribute):
    def __init__(self, age: str):
        super().__init__(3, int(age))

    def _getValue(self) -> str:
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

    def _getValue(self) -> str:
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

    def _getValue(self) -> str:
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

    def _getValue(self) -> str:
        if self.gen_level == 0:
            return self.value
        elif self.gen_level == 1:
            for k, v in self.values.items():
                if self.value in v:
                    return k
        else:
            return "*"


class Occupation:
    value: str
    count = 1

    def __init__(self, value: str):
        self.value = "*" if value == "?" else value

    def __eq__(self, o: object) -> bool:
        if self.value == o.value:
            self.count += o.count
            return True
        return False

    def __lt__(self, other: object) -> bool:
        return self.value.__lt__(other.value)

    def __str__(self) -> str:
        return f"{self.count}x {self.value}"

    def __hash__(self) -> int:
        return self.value.__hash__()