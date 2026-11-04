import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Page setup
st.set_page_config(page_title="Gemini SQL Retriever")
load_dotenv()

# Safely fetch the API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY is missing! Please check your .env file or environment variables.")
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Prompt instructions for Gemini
PROMPT = """You are an SQL expert. SQLite table: Naresh_it_employee (employee_name, employee_role, employee_salary).
Example 1: How many entries? -> SELECT COUNT(*) FROM Naresh_it_employee;
Example 2: Data Science roles? -> SELECT * FROM Naresh_it_employee WHERE employee_role='Data Science';
Return ONLY the raw SQL query without markdown or extra text."""

st.header("Gemini App To Retrieve SQL Data")
model = st.selectbox("Choose Gemini Model", ["gemini-2.5-flash", "gemini-2.5-flash-lite"])
question = st.text_input("Input your question:")

if st.button("Ask the question") and question:
    try:
        # 1. Generate SQL from Gemini
        response = client.models.generate_content(
            model=model, 
            contents=f"{PROMPT}\n\nQuestion: {question}"
        )
        sql = response.text.strip()
        
        # Display generated SQL
        st.subheader("Generated SQL Query")
        st.code(sql, language="sql")

        # 2. Safety check: Ensure it's a SELECT query
        if not sql.lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed for safety.")

        # 3. Execute query on SQLite database
        with sqlite3.connect("Naresh_it_employee.db") as conn:
            cur = conn.execute(sql)
            rows = cur.fetchall()
            cols = [desc[0] for desc in cur.description]

        # 4. Display results
        st.subheader("The Response is")
        if rows:
            data = [dict(zip(cols, row)) for row in rows]
            st.dataframe(data)
        else:
            st.info("The query returned 0 rows.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
