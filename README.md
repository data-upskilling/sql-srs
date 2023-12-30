# SQL-SRS (Spaced Repetition System)

## Project Description

The aim of this project is to create an application to train to sql with [spaced repetition system](https://en.wikipedia.org/wiki/Spaced_repetition), i.e. to be able to practise making
SQL queries with questions recurring at different intervals.

## How to Install the Project

1. Clone the project

2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate
```

3. Install the requirements
```
pip install -r requirements.txt
```

4. Create a folder data and run:
```
python init_db.py
```

## Use Streamlit

To launch the app locally, run:
```
streamlit app.py
```

When the code is pushed on main, the application deployed on streamlit is automatically updated at the address: https://sql-srs-data-upskilling.streamlit.app/
