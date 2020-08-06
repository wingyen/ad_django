## Installation
- install pipenv if you not yet have it.

cd into the directory, then run:
```bash
pipenv shell
pipenv install #install dependencies from Pipfile
python manage.py migrate
python manage.py runserver
```

## API use-cases

1. Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.
http://127.0.0.1:8000/api/adjust/use_cases/?date_to=2017-06-01

2. Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.
http://127.0.0.1:8000/api/adjust/use_cases/?year=2017&month=05&os=ios

3. Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.
http://127.0.0.1:8000/api/adjust/use_cases/?date=2017-06-01&country=us

4. Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order.
http://127.0.0.1:8000/api/adjust/use_cases/?cpi=true&country=us

