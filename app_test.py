import os, sqlite3, streamlit as st
from dotenv import load_dotenv
from google import genai

st.set_page_config(page_title="Gemini SQL Retriever", layout="centered")
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_APIKEY"))
model_choice = st.selectbox("Choose Gemini Model", ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite"])

prompt = """You are an SQL expert. SQLite database table: `Naresh_it_employee` (Columns: employee_name, employee_role, employee_salary).
Example 1: How many entries? -> SELECT COUNT(*) FROM Naresh_it_employee;
Example 2: Data Science roles? -> SELECT * FROM Naresh_it_employee WHERE employee_role='Data Science';
Return ONLY the raw SQL query without markdown or extra text."""

st.header("Gemini App To Retrieve SQL Data")
question = st.text_input("Input your question:", key="input")

if st.button("Ask the question") and question.strip():
    try:
        with st.spinner("Processing..."):
            sql = client.models.generate_content(model=model_choice, contents=f"{prompt}\n\nQuestion: {question}").text.replace("```sql", "").replace("```", "").strip()
            
            st.subheader("Generated SQL Query")
            st.code(sql, language="sql")

            if not sql.lower().startswith("select"): raise ValueError("Only SELECT queries allowed.")
            with sqlite3.connect("Naresh_it_employee.db") as conn:
                cur = conn.cursor()
                rows, cols = cur.execute(sql).fetchall(), [d[0] for d in cur.description]

            st.subheader("The Response is")
            st.dataframe([dict(zip(cols, r)) for r in rows]) if rows else st.info("Returned 0 rows.")
    except Exception as e:
        st.error(f"Error: {e}")