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
    # Fetch the existing data from DB
    existing_data = user_db.get(key=user)
    if existing_data:
        # If user already exists, update the data with new period data
        data = {
            f"{period}": {
            "incomes": incomes,
            "expenses": expenses,
            "comment": comment
            }
        }
        new_data = {
            'data': {
                'period': existing_data.get('data', {}).get('period', []) + [data]
            }
        }
        user_db.update(
            key=user,
            updates= new_data
        )

    else:
        # Add records for new users
        data = {
            "period": [
                {
                    f"{period}": {
                    "incomes": incomes,
                    "expenses": expenses,
                    "comment": comment
                    }
                }
            ]
        }
        # Insert the data to the Base
        user_db.put({
            "key": user,
            "data": data
        })

def fetch_all_users():
    res = user_db.fetch()
    users = [user['key'] for user in res.items]
    return users

def fetch_user_data(user):
    res = user_db.fetch(query={'key': user}).items
    periods = [(list(month.keys())[0], list(month.values())[0]) for month in res[0]['data']['period']]
    records = {key: value for key, value in periods}
    return records