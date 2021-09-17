# py 3.9.6

"""
    CS528 - Data Privacy and Security
    Illinois Institute of Technology
    Homework 1
    9-15-21
    
    Attr.py
    
    All the attributes are converted into classes to help with the generalization and organization of each attribute
"""

# Total number of attributes, used for distortion and percision calculations
TOTAL_ATTRIBUTES = 4

# The class that all attributes extend
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

    # Update qualifier values, qualifiers including distortion and precision numerator and the generalization level
    def _setQualifiers(self):
        self.distortion = (self.gen_level / self.gen_max) / TOTAL_ATTRIBUTES
        self.precision_num = self.gen_level / self.gen_max  # h / |DGH_Ai|
        self.gen_value = self._getValue()

    # Set the specific generalization level of this attribute
    def setGenLevel(self, gen: int):
        self.gen_level = max(0, min(gen, self.gen_max))
        self._setQualifiers()

    # Increase the generalization level of this attribute
    def upGenLevel(self):
        self.setGenLevel(self.gen_level + 1)

    # Decrease the generalization level of this attribute
    def downGenLevel(self):
        self.setGenLevel(self.gen_level - 1)

    # Generate and return the value, which is generalized to the level that is set
    # This func should be extended, else it just returns the actual private value
    def _getValue(self) -> str:
        return self.value

    # Return the current value, which is generalized to the level that is set
    def getValue(self) -> str:
        return self.gen_value


# Age is not a categorical value, meaning it has no predefined hierarchy and is only implemented in _getValue
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


# Categorical value which uses a predefined hierarchy to generalize values
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

    def _getValue(self) -> str:  # IMPROVE: Categorical values could probably have _getValue generalized
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


# Categorical value which uses a predefined hierarchy to generalize values
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


# Categorical value which uses a predefined hierarchy to generalize values
class Race(Attribute):

    values = {
        "white": (  # NOTE: A significant portion of the data set is White ( nearly half ) which is why the generalization is between white and non-white
            "White"
        ),
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