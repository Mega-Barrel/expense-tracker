import calendar # Core Python Module
from datetime import datetime # Core Python Module

import streamlit as st # pip install streamlit
from streamlit_option_menu import option_menu # pip install streamlit-option-menu
import plotly.graph_objects as go # pip install plotyl

import database as db # Local import

# -------------- SETTINGS --------------
incomes = ['Salary', 'Blog', 'Other Income']
expenses = ['Rent', 'Utilities', 'Groceries', 'Car', 'Other Expenses', 'Saving']
currency = '$'
page_title = 'Income and Expense Tracker'
page_icon = ':money_with_wings:'
layout = 'centered'
# ---------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon,layout=layout)
st.title(page_title + " " + page_icon)

# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
years = [datetime.today().year, datetime.today().year - 1]
months = list(calendar.month_name[1:])

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)


# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization"],
    icons=["pencil-fill", "bar-chart-fill"], # https//:icons.getbootstrap.com/
    orientation="horizontal",
)

# --- INPUT AND SAVE PERIODS ---
if selected == 'Data Entry':
    st.header(f'Data Entry in {currency}')
    with st.form("entry_form", clear_on_submit=True):
        name = st.text_input('Enter your name:')
        # Create 2 colums for Month and year entry
        col1, col2 = st.columns(2)
        col1.selectbox("Select Month: ", months, key='month')
        col2.selectbox("Select Year: ", years, key='year')
        "---"
        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}: ", min_value=0, format="%i", step=10, key=income)

        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense}: ", min_value=0, format="%i", step=10, key=expense)

        with st.expander("Comments"):
            comment = st.text_area("", placeholder="Enter a comment here...")

        submitted = st.form_submit_button("Save Data") 
        if submitted:
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {expense: st.session_state[expense] for expense in expenses}
            db.insert_period(name, period, incomes, expenses, comment)
            st.success("Data Saved!")

# --- PLOT PERIODS ---
if selected == 'Data Visualization':
    st.header("Data Visualization")

    with st.form("saved_periods"):
        name = st.selectbox("Select User: ", db.fetch_all_users())
        usr_submit = st.form_submit_button("Get User Periods")
        # Get the selected user period
        usr_data = db.fetch_user_data(user=name)
        period = st.selectbox("Select Period: ", list(usr_data.keys()))
        submitted = st.form_submit_button("Plot Period")
        if submitted:
            # Get Data from database
            comment = usr_data[period].get('comment')
            expenses = usr_data[period].get('expenses')
            incomes = usr_data[period].get('incomes')
            income = usr_data[period].get('period')

            # Create Metrics
            total_income = sum(incomes.values())
            total_expense = sum(expenses.values())
            remaining_budget = total_income - total_expense
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f'{total_income} {currency}')
            col2.metric("Total Expense", f'{total_expense} {currency}')
            col3.metric("Remaining Budget", f'{remaining_budget} {currency}')
            st.text(f"Comments: {comment}")
            
            # Create Sankey Chart
            label = list(incomes.keys()) + ['Total Income'] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses]
            value = list(incomes.values()) + list(expenses.values())
            
            # Data to dict, dict to sankey
            link = dict(source=source, target = target, value=value)
            node = dict(label=label, pad=20, thickness=30, color='#E694FF')
            data = go.Sankey(link=link, node=node)
            
            # Plot it!
            st.write(f'Plotting data for {period} Period.')
            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)