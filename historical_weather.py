"""
Historical Weather Analysis.
Perform a calculation on historical weather data: the greatest daily temperature change for a particular city, or the average yearly days of precipitation for a particular city.

Base code by Caden Howell<cadenhowell@gmail.com>
Claude 3.7 Sonnet was used in the Cody plugin in Pycharm for suggested line completions and some debugging.
"""
import argparse
import sys
import pandas as pd

FILENAME = "data/noaa_historical_weather_10yr.csv"

STATION_MAP = {
    "bos": "USW00014739",
    "jnu": "USW00025309",
    "mia": "USW00012839"
}


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Perform a calculation on historical weather data: the greatest daily temperature change for a particular city, or the average yearly days of precipitation for a particular city.")
    parser.add_argument("function_name", help="Required. Either max-temp-delta or days-of-precip")
    parser.add_argument("-c", "--city", type=str, help="Required. Which city to evaluate: bos, jnu, or mia")
    parser.add_argument("-y", "--year", type=int,
                        help="(max-temp-delta only) Optional.  Restrict search to a particular year in the range 2010-2019.")
    parser.add_argument("-m", "--month", type=int,
                        help="(max-temp-delta only) Optional.  Restrict search to a particular month in the range 1-12.)  Requires a year.")
    parser.add_argument("-f", "--filename", type=str, default=FILENAME,
                        help=f"Optional. Filename, defaults to {FILENAME}")
    parser.add_argument("-v", "--verbose", action='store_true',
                        help="Optional. Print more output than just the solution.")

    args = parser.parse_args()
    validate_args(args)

    if args.verbose:
        print("Verbose output enabled.")

        if args.function_name is not None:
            print(f"Function name: {args.function_name}")
        if args.city is not None:
            print(f"City: {args.city}, maps to {STATION_MAP[args.city]}")
        if args.year is not None:
            print(f"Year: {args.year}")
        if args.month is not None:
            print(f"Month: {args.month}")

    return args


def validate_args(args):
    """Validate command line arguments."""
    valid_args = True

    if args.function_name not in ['max-temp-delta','days-of-precip']:
        print("Function name must be either max-temp-delta or days-of-precip")
        valid_args = False

    if args.month is not None:
        if args.function_name != 'max-temp-delta':
            print("Function name must be max-temp-delta to specify a month.")
            valid_args = False
        if args.year is None:
            print("Specifying a month requires a year.")
            valid_args = False
        if args.month < 1 or args.month > 12:
            print("Month must be between 1 and 12.")
            valid_args = False

    if args.year is not None:
        if args.function_name != 'max-temp-delta':
            print("Function name must be max-temp-delta to specify a year.")
            valid_args = False
        if args.year < 2010 or args.year > 2019:
            print("Year must be between 2010 and 2019.")
            valid_args = False

    if args.city is not None:
        if args.city not in ['bos', 'jnu', 'mia']:
            print("City must be either bos, jnu, or mia.")
            valid_args = False
    else:
        print("City must be specified.")
        valid_args = False

    if not valid_args:
        sys.exit(1)


def verbose_out(args, message):
    """Print message if verbose output is enabled."""
    if args.verbose is True:
        print(message)


def days_of_precip(df, args):
    """Calculate the average number of days of precipitation for a city.  Print the result and return it."""
    # make new combined precipitation row
    df['SNOW'] = df['SNOW'].fillna(0)
    df['PRCP'] = df['PRCP'].fillna(0)
    df["TOTAL_PRECIP"] = df["PRCP"] + df["SNOW"]
    verbose_out(args, "With total precipitation:")
    verbose_out(args, df.head())
    # filter to days with non-zero total precipitation
    df = df[df["TOTAL_PRECIP"] > 0]
    # count up by year
    df = df.groupby(["YEAR"]).count()
    verbose_out(args, "Grouped by year:")
    verbose_out(args, df.head())
    average_days = df["TOTAL_PRECIP"].mean()
    print(f"days_of_precip: {average_days:.1f}")
    # We are printing instead of using the result, but normally it seems like a function like this would return it.
    return average_days


def max_temp_delta(df, args):
    """Calculate the greatest daily temperature change for a city.  Print the result and return it."""
    # filter to year, month
    if args.year is not None:
        df = df[df["YEAR"] == args.year]
    if args.month is not None:
        df = df[df["MONTH"] == args.month]

    # Make a copy of the DataFrame to avoid SettingWithCopyWarning
    df = df.copy()
    # Alternatively, use the Pandas 3 feature which will handle this for us.
    # pd.options.mode.copy_on_write = True

    # make a new column with temp delta
    df["TEMP_DELTA"] = df["TMAX"] - df["TMIN"]
    verbose_out(args, "With temp delta:")
    verbose_out(args, df.head())
    max_delta = df["TEMP_DELTA"].max()
    print(f"max_temp_delta: {max_delta:.1f}")
    # We are printing instead of using the result, but normally it seems like a function like this would return it.
    return max_delta


def main():
    # Process the file and options
    args = parse_args()
    verbose_out(args, "Processing file...")

    df = pd.read_csv(f"{args.filename}")
    # Drop unused columns
    df = df[["PRCP", "SNOW", "TMAX", "TMIN", "STATION", "DATE"]]

    # All cases are limited by city
    station_code = STATION_MAP[args.city]
    df = df[df["STATION"] == station_code]
    # We need month and year
    df["DATE"] = pd.to_datetime(df["DATE"])
    df["MONTH"] = df["DATE"].dt.month
    df["YEAR"] = df["DATE"].dt.year
    verbose_out(args, "Data sample:")
    verbose_out(args, df.head())
    if args.function_name == "days-of-precip":
        days_of_precip(df, args)
    if args.function_name == "max-temp-delta":
        max_temp_delta(df, args)


if __name__ == "__main__":
    main()