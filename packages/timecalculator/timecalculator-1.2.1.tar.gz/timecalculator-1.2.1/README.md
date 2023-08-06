TimeCalculator

The TimeCalculator package is a Python package for converting time units to seconds. It provides a TimeCalculator class that can be used to convert any time unit to seconds, not just the predefined time units.

### Features

The TimeCalculator package provides the following features:

- Conversion of any time unit to seconds using the TimeCalculator class
- Predefined time units for convenience, including:
  - `MINUTE`: number of seconds in a minute
  - `HOUR`: number of seconds in an hour
  - `DAY`: number of seconds in a day
  - `WEEKEND`: number of seconds in a weekend (2 days)
  - `WORK_WEEK`: number of seconds in a work week (5 days)
  - `WEEK`: number of seconds in a week
  - `MONTH`: number of seconds in a month (30 days)
  - `YEAR`: number of seconds in a year (365 days)

### Installation

The TimeCalculator package can be installed via pip:

```
pip install timecalculator
```

### Usage

To use the TimeCalculator package, you first need to create a TimeCalculator object:

```

from timecalculator import TimeCalculator
tc = TimeCalculator()

```

Once you have a TimeCalculator object, you can use the `to_seconds` method to convert any time unit to seconds. The `to_seconds` method takes two arguments: `time_value` and `time_unit`. The `time_value` argument is the value you want to convert, and the `time_unit` argument is the unit of the value, expressed in seconds.

Here's a simple example of how to use the `to_seconds` method to convert 5 minutes to seconds:

```

minutes = 5
total_seconds = tc.to_seconds(minutes, tc.MINUTE)
print(f"{minutes} minutes is {total_seconds} seconds")

```

In this example, we pass the value `5` and the `MINUTE` constant to the `to_seconds` method to convert the time to seconds. The resulting value is stored in the `total_seconds` variable. Finally, we print out the result.

The output of this code will be:

`5 minutes is 300 seconds`

### API Reference

The TimeCalculator class provides the following methods and attributes:

#### `to_seconds(time_value: float, time_unit: int) -> float`

Convert a time value from one unit to another.

- `time_value` (float): The value to convert.
- `time_unit` (int): The unit of the value, in seconds.

Returns:

- `float`: The converted value, in seconds.

#### Predefined Time Units

The TimeCalculator class provides the following predefined time units for convenience:

- `MINUTE` (int): Number of seconds in a minute.
- `HOUR` (int): Number of seconds in an hour.
- `DAY` (int): Number of seconds in a day.
- `WEEKEND` (int): Number of seconds in a weekend (2 days).
- `WORK_WEEK` (int): Number of seconds in a work week (5 days).
- `WEEK` (int): Number of seconds in a week.
- `MONTH` (int): Number of seconds in a month (30 days).
- `YEAR` (int): Number of seconds in a year (365 days).

### Contributions

Contributions to the TimeCalculator package are welcome.
