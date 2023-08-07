# OpenWeather Report

Get weather using OpenWeather API and save to a database.

## Quickstart

To install, you can use `pipx`:

```
$ pipx install openweather_report
```

If using `pip` I would suggest installing into a virtual environment.
**Note** that `libpq` is required for `psycopg2`.
Below is how to install using a Debian based distro like Ubuntu:

```
$ sudo apt install install libpq-dev libpq5
```

Then you can install `openweather_report`.
Then to get help, do:

```
$ openweather_report --help
Usage: openweather_report [OPTIONS] {one_call}
                          LATITUDE LONGITUDE API_KEY

  Take user inputs and save to either file or database.

Options:
  --weather_date [%Y-%m-%d %H:%M]
                                  Put in the date to get the weather for a
                                  particular day.
  --save [json|postgresql|sqlite]
  --save_path TEXT
  --db_string TEXT                Connection string to save to database.
  --version                       Show the version and exit.
  --help                          Show this message and exit.
```

To save data to a json file:

```
$ openweather_report one_call 30.00 -30.00 your-api-key --save json --save_path
my_city.json
```

## Setting up Database Structure

Currently PostgreSQL and Sqlite are supported.
The table structure will need to be generated before attempting to save any
data.

### PostgreSQL

Below is the structure for `raw_json_data`:

```
create schema if not exists weather;

create table if not exists weather.raw_json_data (
(
     id bigserial not null
    ,entry_date timestamp with time zone not null
    ,api_call text not null
    ,raw_data jsonb null
    ,software_version null
	,primary key (id)
);
```

### SQLite

The structure is similar to PostgreSQL but does not have a schema:

```
create table if not exists raw_json_data
(
     id integer primary key
    ,entry_date text not null
    ,api_call text not null
    ,raw_data text null
    ,software_version text null
);
```

## OpenWeather API

Go to https://openweathermap.org/api though this program currently only
supports the One Call API.
The program will eventually support other APIs.
