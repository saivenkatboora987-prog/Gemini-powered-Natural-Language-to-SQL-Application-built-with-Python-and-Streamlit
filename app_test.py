import streamlit as st
import sqlite3
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Must be the first Streamlit command
st.set_page_config(page_title="I can Retrieve Any SQL query")

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_APIKEY"))

# Replace these with model names printed by your list_models.py
model_choice = st.selectbox(
    "Choose Gemini Model",
    ["YOUR-FLASH-MODEL-1", "YOUR-FLASH-MODEL-2"]
)

def get_gemini_response(question, prompt, model_choice):
    model = genai.GenerativeModel(model_choice)
    response = model.generate_content([prompt[0], question])
    # Remove any code fences or "sql" label Gemini might add
    text = response.text.strip()
    text = text.replace("```sql", "").replace("```", "").strip()
    return text

def read_sql_query(sql, db):
    # Only allow read-only queries
    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    columns = [d[0] for d in cur.description]
    conn.close()
    return rows, columns

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
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit:
    if not question.strip():
        st.warning("Please type a question first.")
    else:
        try:
            sql_query = get_gemini_response(question, prompt, model_choice)

            st.subheader("Generated SQL Query")
            st.code(sql_query, language="sql")

            rows, columns = read_sql_query(sql_query, "Naresh_it_employee.db")

            st.subheader("The Response is")
            st.dataframe([dict(zip(columns, row)) for row in rows])
        except Exception as e:
            st.error(f"Something went wrong: {e}")