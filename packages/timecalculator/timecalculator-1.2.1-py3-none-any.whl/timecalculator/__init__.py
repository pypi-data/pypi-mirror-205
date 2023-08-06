import time
from dataclasses import dataclass


@dataclass
class TimeCalculator:
    """
    A class for converting time units.

    Example usage:
    ```
    tc = TimeCalculator()
    hours = 1
    seconds = tc.to_seconds(hours, TimeCalculator.HOUR)
    print(f"{hours} hour(s) is {seconds} second(s)")
    ```

    Attributes:
    MINUTE (int): Number of seconds in a minute.
    HOUR (int): Number of seconds in an hour.
    DAY (int): Number of seconds in a day.
    WEEKEND (int): Number of seconds in a weekend (2 days).
    WORK_WEEK (int): Number of seconds in a work week (5 days).
    WEEK (int): Number of seconds in a week.
    MONTH (int): Number of seconds in a month (30 days).
    YEAR (int): Number of seconds in a year (365 days).
    """

    MINUTE: int = 60
    HOUR: int = 60 * MINUTE
    DAY: int = 24 * HOUR
    WEEKEND: int = 2 * DAY
    WORK_WEEK: int = 5 * DAY
    WEEK: int = 7 * DAY
    MONTH: int = 30 * DAY
    YEAR: int = 365 * DAY

    @classmethod
    def sys_time(cls) -> str:
        """
        Get the current system time as a string.

        Returns:
        str: The current system time in the format "Mon, DD MMM YYYY, HH:MM:SS".
        """
        return time.strftime("%a, %d %b %Y, %H:%M:%S", time.localtime())

    @staticmethod
    def to_seconds(time_value: float, time_unit: int) -> float:
        """
        Convert a time value from one unit to another.

        Args:
        time_value (float): The value to convert.
        time_unit (int): The unit of the value, in seconds.

        Returns:
        float: The converted value, in seconds.

        Example:
        ```
        tc = TimeCalculator()
        hours = 1
        seconds = tc.to_seconds(hours, TimeCalculator.HOUR)
        print(f"{hours} hour(s) is {seconds} second(s)")
        ```
        """
        if not isinstance(time_value, (int, float)):
            raise TypeError(f"time_value={time_value} is not a valid type (should be int or float)")
        return time_value * time_unit
