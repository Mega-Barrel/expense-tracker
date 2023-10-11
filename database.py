import os # python core module
from deta import Deta # pip install deta
from dotenv import load_dotenv # pip install python-dotenv

load_dotenv('.env')

DETA_KEY = os.environ['project_key']

# Initialize with a project key
deta = Deta(DETA_KEY)

# Database Connection
db = deta.Base("monthly_reports")

# Insert data into table
def insert_period(period, incomes, expenses, comment):
    """Returns the report on a successful creation, otherwise raises an error."""
    return db.put({
        "key": period,
        "incomes": incomes,
        "expenses": expenses,
        "comment": comment
    })
    
# Fetch all periods
def fetch_all_periods():
    """Returns a dict of all periods"""
    res = db.fetch()
    return res.items

# Fetch data by period
def get_period(period):
    """If not found, the function will return None"""
    return db.get(period)

# Fetch all periods
def get_all_periods():
    items = fetch_all_periods()
    periods = [item['key'] for item in items]
    return periods