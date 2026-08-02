import streamlit as st
import sqlite3
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
# Provide your GenAI API Key

genai.configure(api_key=os.getenv('GEMINI_APIKEY'))

# 🔽 Add dropdown here (right after API key config)
# Add dropdown here (right after API key config)
model_choice = st.selectbox(
    "Choose Gemini Model",
    ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite"]
)

def get_gemini_response(question, prompt, model_choice):
    model = genai.GenerativeModel(model_choice)
    response = model.generate_content([prompt[0], question])
    return response.text

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

## Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name Naresh_it_employee and has the following columns - employee_name, 
    employee_role, employee_salary \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM Naresh_it_employee ;
    \nExample 2 - Tell me all the employees working in Data Science role?, 
    the SQL command will be something like this SELECT * FROM Naresh_it_employee 
    where employee_role="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

## Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(question, prompt, model_choice)

    # Show the generated SQL query
    st.subheader("Generated SQL Query")
    st.code(response, language="sql")

    # Run the query
    response = read_sql_query(response, "Naresh_it_employee.db")

    st.subheader("The Response is")
    for row in response:
        st.write(row)
