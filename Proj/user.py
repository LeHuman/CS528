"""module containing user related things"""

import datetime


def convert_dataset_date(date: str, short: bool = False) -> datetime:
    """Create a datetime object from a dataset date

    Args:
        date (str): date str from the dataset

    Returns:
        datetime: datetime representing the date str
    """
    return datetime.datetime.strptime(date, "%m/%d/%Y" if short else "%m/%d/%Y %I:%M:%S %p")


class UserEntry:
    """Abstract for User entries"""


class DailyActivity(UserEntry):
    """Daily activity entry"""

    activity_date: datetime.datetime
    total_steps: int
    total_distance: float
    tracker_distance: float
    logged_activities_distance: float
    very_active_distance: float
    moderately_active_distance: float
    light_active_distance: float
    sedentary_active_distance: float
    very_active_minutes: int
    fairly_active_minutes: int
    lightly_active_minutes: int
    sedentary_minutes: int
    calories: int

    def __init__(
        self,
        activity_date: str,
        total_steps: int,
        total_distance: float,
        tracker_distance: float,
        logged_activities_distance: float,
        very_active_distance: float,
        moderately_active_distance: float,
        light_active_distance: float,
        sedentary_active_distance: float,
        very_active_minutes: int,
        fairly_active_minutes: int,
        lightly_active_minutes: int,
        sedentary_minutes: int,
        calories: int,
    ):
        self.activity_date = convert_dataset_date(activity_date, True)
        self.total_steps = int(total_steps)
        self.total_distance = float(total_distance)
        self.tracker_distance = float(tracker_distance)
        self.logged_activities_distance = float(logged_activities_distance)
        self.very_active_distance = float(very_active_distance)
        self.moderately_active_distance = float(moderately_active_distance)
        self.light_active_distance = float(light_active_distance)
        self.sedentary_active_distance = float(sedentary_active_distance)
        self.very_active_minutes = int(very_active_minutes)
        self.fairly_active_minutes = int(fairly_active_minutes)
        self.lightly_active_minutes = int(lightly_active_minutes)
        self.sedentary_minutes = int(sedentary_minutes)
        self.calories = int(calories)


class HourlyActivity(UserEntry):
    """Hourly activity entry"""

    activity_date: datetime.datetime
    calories: int
    total_intensity: int
    average_intensity: float
    total_steps: int

    def __init__(self, activity_date: str, calories: int, total_intensity: int, average_intensity: float, total_steps: int):
        self.activity_date = convert_dataset_date(activity_date)
        self.calories = int(calories)
        self.total_intensity = total_intensity
        self.average_intensity = average_intensity
        self.total_steps = total_steps


class HeartRate(UserEntry):
    """Heartrate Entry"""

    activity_date: datetime.datetime
    rate: int

    def __init__(self, activity_date: str, rate: int):
        self.activity_date = convert_dataset_date(activity_date)
        self.rate = int(rate)


class SleepTime(UserEntry):
    """Sleep Time Entry"""

    activity_date: datetime.datetime
    total_sleep_records: int
    total_minutes_asleep: int
    total_time_in_bed: int

    def __init__(self, activity_date: str, total_sleep_records: int, total_minutes_asleep: int, total_time_in_bed: int):
        self.activity_date = convert_dataset_date(activity_date)
        self.total_sleep_records = total_sleep_records
        self.total_minutes_asleep = total_minutes_asleep
        self.total_time_in_bed = total_time_in_bed


class User:
    """User data class for fitbit data"""

    id_num: int
    daily_activities: list[DailyActivity]
    hourly_activities: list[HourlyActivity]
    sleep_times: list[SleepTime]
    heart_rates: list[HeartRate]

    def __init__(self, id_num: int) -> None:
        self.id_num = id_num
        self.daily_activities = []
        self.hourly_activities = []
        self.sleep_times = []
        self.heart_rates = []

    def __hash__(self) -> int:
        return self.id_num

    def __str__(self) -> str:
        return f"ID: {self.id_num}\n\tDaily entries: {len(self.daily_activities)}\n\tHourly entries: {len(self.hourly_activities)}\n\tSleep entries: {len(self.sleep_times)}\n\tHeart entries: {len(self.heart_rates)}"

    def add_entry(self, entry: UserEntry):
        """Add a user entry to this User

        Args:
            entry (UserEntry): The user entry object
        """
        match entry.__class__.__name__:
            case DailyActivity.__name__:
                self.daily_activities.append(entry)
            case HourlyActivity.__name__:
                self.hourly_activities.append(entry)
            case SleepTime.__name__:
                self.sleep_times.append(entry)
            case HeartRate.__name__:
                self.heart_rates.append(entry)
            case _:
                raise Exception("Invalid class type")
