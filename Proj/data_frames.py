import time
import datetime
import pandas as pd
import numpy as np

from pandas.core.frame import DataFrame
from pathos.pools import ProcessPool as Pool

# Data Frame Indexes - Used for easier indexing of values
FRAME_ID = "Id"
FRAME_TIME = "Time"


class ENTRY(str):
    pass


class FIELD(str):
    ENTRY: str
    TYPE: type


def NEW_FIELD(entry: str, val: str, TYPE: type) -> FIELD:
    val = FIELD(val)
    val.ENTRY = entry
    val.TYPE = TYPE
    return val


class DAILY(ENTRY):
    VALUE = "daily"

    CALORIES = NEW_FIELD("daily", "Calories", int)
    TOTAL_STEPS = NEW_FIELD("daily", "TotalSteps", int)
    TOTAL_DISTANCE = NEW_FIELD("daily", "TotalDistance", float)
    TRACKER_DISTANCE = NEW_FIELD("daily", "TrackerDistance", float)
    LOGGED_ACTIVITIES_DISTANCE = NEW_FIELD("daily", "LoggedActivitiesDistance", float)
    VERY_ACTIVE_DISTANCE = NEW_FIELD("daily", "VeryActiveDistance", float)
    MODERATELY_ACTIVE_DISTANCE = NEW_FIELD("daily", "ModeratelyActiveDistance", float)
    LIGHT_ACTIVE_DISTANCE = NEW_FIELD("daily", "LightActiveDistance", float)
    SEDENTARY_ACTIVE_DISTANCE = NEW_FIELD("daily", "SedentaryActiveDistance", float)
    VERY_ACTIVE_MINUTES = NEW_FIELD("daily", "VeryActiveMinutes", int)
    FAIRLY_ACTIVE_MINUTES = NEW_FIELD("daily", "FairlyActiveMinutes", int)
    LIGHTLY_ACTIVE_MINUTES = NEW_FIELD("daily", "LightlyActiveMinutes", int)
    SEDENTARY_MINUTES = NEW_FIELD("daily", "SedentaryMinutes", int)


class HEART(ENTRY):
    VALUE = "heart"

    BPM = NEW_FIELD("heart", "Value", int)


class SLEEP(ENTRY):
    VALUE = "sleep"

    TOTAL_SLEEP_RECORDS = NEW_FIELD("sleep", "TotalSleepRecords", int)
    TOTAL_MINUTES_ASLEEP = NEW_FIELD("sleep", "TotalMinutesAsleep", int)
    TOTAL_TIME_IN_BED = NEW_FIELD("sleep", "TotalTimeInBed", int)


class HOURLY(ENTRY):
    VALUE = "hourly"

    CALORIES = NEW_FIELD("hourly", "Calories", int)
    TOTAL_INTENSITY = NEW_FIELD("hourly", "TotalIntensity", int)
    AVERAGE_INTENSITY = NEW_FIELD("hourly", "AverageIntensity", float)
    STEP_TOTAL = NEW_FIELD("hourly", "StepTotal", int)


def convert_dataset_date(date: str, short: bool = False) -> float:
    """Create a datetime object from a dataset date

    Args:
        date (str): date str from the dataset

    Returns:
        float: UNIX Timestamp representing the date str
    """

    return time.mktime(datetime.datetime.strptime(date, "%m/%d/%Y" if short else "%m/%d/%Y %I:%M:%S %p").timetuple())


def tick():
    print("|", end="", flush=True)


def parallel_apply(data, func, num_of_processes=6):
    data_split = np.array_split(data, num_of_processes)
    with Pool(num_of_processes) as p:
        return pd.concat(p.map(lambda chunk: chunk.apply(func), data_split))


def daily_frame() -> DataFrame:
    daily_df = pd.read_csv("dataset/dailyActivity_merged.csv")

    tick()
    daily_df = daily_df.rename(columns={"ActivityDate": FRAME_TIME})
    daily_df[FRAME_TIME] = parallel_apply(daily_df[FRAME_TIME], lambda x: convert_dataset_date(x, True))

    tick()
    return daily_df


def heart_frame() -> DataFrame:
    heart_df = pd.read_csv("dataset/heartrate_seconds_merged.csv")

    tick()
    heart_df = heart_df.rename(columns={"Time": FRAME_TIME})
    heart_df[FRAME_TIME] = parallel_apply(heart_df[FRAME_TIME], convert_dataset_date)

    tick()
    return heart_df


def sleep_frame() -> DataFrame:
    sleep_df = pd.read_csv("dataset/sleepDay_merged.csv")

    tick()
    sleep_df = sleep_df.rename(columns={"SleepDay": FRAME_TIME})
    sleep_df[FRAME_TIME] = parallel_apply(sleep_df[FRAME_TIME], convert_dataset_date)

    tick()
    return sleep_df


def hourly_frame() -> DataFrame:
    hourly_cal: DataFrame = pd.read_csv("dataset/hourlyCalories_merged.csv")
    hourly_int: DataFrame = pd.read_csv("dataset/hourlyIntensities_merged.csv")
    hourly_stp: DataFrame = pd.read_csv("dataset/hourlySteps_merged.csv")

    tick()
    hourly_df = hourly_cal.merge(hourly_int, "left", (FRAME_ID, "ActivityHour")).merge(hourly_stp, "left", (FRAME_ID, "ActivityHour"))
    hourly_df = hourly_df.rename(columns={"ActivityHour": FRAME_TIME})

    tick()
    hourly_df[FRAME_TIME] = parallel_apply(hourly_df[FRAME_TIME], convert_dataset_date)

    tick()
    return hourly_df
