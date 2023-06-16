Python script for preprocessing online raw data for the purpose of feeding Only-PhD.

# Folders/Files

- [`/raw`](/raw) stores raw `.json` or `.csv` data from online.
- [`db.py`](db.py) handles db connection and migrations. Since the data volume is small, [sqlite3](https://docs.python.org/3/library/sqlite3.html) is used.
- [`types.py`](types.py) serves as data validators before saving data in the database.

# Dev Setup

- (Recommended) Set up your virtual environment.
- Install `pip-tools` as the first dependency.
- Run `pip-compile requirements.in` to generate an up-to-date `requirements.txt` file.
- Execute `pip install -r requirements.txt` to install the dependencies.

# Usage

- Check out `python main.py --help`
