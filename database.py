import os # python core module
from deta import Deta # pip install deta
from dotenv import load_dotenv # pip install python-dotenv

load_dotenv('.env')

DETA_KEY = os.environ['project_key']

# Initialize with a project key
deta = Deta(DETA_KEY)

# Database Connection
user_db = deta.Base("user_reports")

# Insert data into table
def insert_period(user, period, incomes, expenses, comment):
    """Returns the report on a successful creation, otherwise raises an error."""
    return user_db.put({
        "key": user,
        "period": [period],
        "incomes": incomes,
        "expenses": expenses,
        "comment": comment
    })

def fetch_all_users():
    res = user_db.fetch()
    users = [user['key'] for user in res.items]
    return users

def fetch_user_periods(user):
    res = user_db.fetch(query={'key': user})
    periods = [item['period'] for item in res.items]
    return periods

def fetch_user_period_data(user, period):
    res = user_db.fetch(query={'key': user, 'period': period})
    return res.items