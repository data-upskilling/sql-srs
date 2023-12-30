# pylint: disable=missing-module-docstring
import os
import logging
from datetime import date, timedelta

import duckdb
import streamlit as st

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
    # subprocess.run (["python","init_db.py"])


def check_users_solution(query: str) -> None:
    """
    Checks that user SQL query is correct by
    1: checking the lines and columns number
    2: checking the values
    param query: a strIg containing the query inserted by the user!
    """
    result = con.execute(query).df()
    st.dataframe(result)
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.text("Bravo c'est correct!")
            st.balloons()
    except KeyError as e:
        st.write("Some columns are missing")


con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

st.write(
    """
   # SQL SRS
   Spaced Repetition System
   """
)

with st.sidebar:
    available_theme = con.execute("SELECT DISTINCT theme FROM memory_state").df()

    theme = st.selectbox(
        "What would you like to review?",
        list(available_theme["theme"]),
        index=None,
        placeholder="Select a theme...",
    )

    st.write("You selected:", theme)

    if theme:
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"

    else:
        select_exercise_query = f"SELECT * FROM memory_state"

    exercise = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("Last_reviewed")
        .reset_index(drop=True)
    )

    exercise_name = exercise.loc[0, "exercise_name"]

    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()


sql_query = st.text_area(label="Enter your SQL code")

if sql_query:
    check_users_solution(sql_query)

for n_days in [2, 7, 21]:
    if st.button(f"Review in {n_days} jours"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(
            f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name= '{exercise_name}'"
        )
        st.rerun()

if st.button("Reset"):
    con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()

tab2, tab3 = st.tabs(["Tables", "Answers"])

with tab2:
    exercises_table = exercise.loc[0, "tables"]
    for table in exercises_table:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)
    st.write("expected:")
    st.dataframe(solution_df)

with tab3:
    st.text(answer)
