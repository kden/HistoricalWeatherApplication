
# Historical Weather Application

## Requirements

- uv
- Python 3.11 or above
- Pandas

## Usage

From the command line, use uv to run the program.  For example, 
```
uv run historical_weather.py -h
```


The usage instructions are summed up by the results of running the script with the `-h` flag.
The only difference is that it is not necessary to put `function_name` last.  You can put it first as it was done in the project instructions.

```bash
usage: historical_weather.py [-h] [-c CITY] [-y YEAR] [-m MONTH] [-f FILENAME] [-v] function_name

Perform a calculation on historical weather data: the greatest daily temperature change for a particular city, or
the average yearly days of precipitation for a particular city.

positional arguments:
  function_name         Required. Either max-temp-delta or days-of-precip

options:
  -h, --help            show this help message and exit
  -c CITY, --city CITY  Required. Which city to evaluate: bos, jnu, or mia
  -y YEAR, --year YEAR  (max-temp-delta only) Optional. Restrict search to a particular year in the range
                        2010-2019.
  -m MONTH, --month MONTH
                        (max-temp-delta only) Optional. Restrict search to a particular month in the range
                        1-12.) Requires a year.
  -f FILENAME, --filename FILENAME
                        Optional. Filename, defaults to data/noaa_historical_weather_10yr.csv
  -v, --verbose         Optional. Print more output than just the solution.
```

## Design choices

- **Modules or one file?**  For such a small script, I decided to use a single file.  As the script grows, I would review the structure and start breaking it into modules.  In this script the code is generally grouped into input handling and calculations, so I would expect the first refactoring to organize the code along those lines.
- **Type hints?**  I like type hints.  I didn't put them in to cut down on time spent on the assignment.  I also find them helpful when reading large code bases to help me see where data flows in and out of of methods and functions.  For a short script like this where we have a good sense of the data types from the easy to understand numeric concepts (temperature and rainfall instead of, say, n-dimensional matrices of abstract values) I didn't prioritize it.
- **Rounding?**  I went with 1 decimal, since the input file seems to be to 1 decimal for the values used.
- **Pandas or just Python?**  I went out on a limb and assumed you use Pandas, and that I should show some basic understanding of it. This arithmetic could have been done with arrays and loops and avoided including the sizable Pandas library.  However, there are a lot of succinct and reusable Pandas features, like the ability to import a CSV file in one line, and support for complicated math. Should this script be expanded, it's likely that those would be helpful.
- **Testing?**  I tested the code manually and compared the results to calculations performed in LibreOffice Calc.  It needs unit tests!  I would probably generate a first draft with an AI coding tool and update it to test that:
  - Arguments are parsed correctly
  - Bad arguments cause the program to exit without blowing up, and give useful feedback
  - Calculations are correct
