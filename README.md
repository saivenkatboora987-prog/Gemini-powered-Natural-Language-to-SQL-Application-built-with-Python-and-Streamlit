# Natural Language to SQL with Gemini

A Streamlit app that converts plain-English questions into SQL queries using Google's Gemini API, runs them on a database, and shows the results instantly.

## Demo

[![App Screenshot](screenshots/demo.png)](https://github.com/saivenkatboora987-prog/Gemini-powered-Natural-Language-to-SQL-Application-built-with-Python-and-Streamlit/blob/main/sql.png?raw=true)


## Features

- Ask questions in plain English, no SQL knowledge needed
- Gemini generates the matching SQL query
- Runs the query on a [SQLite / MySQL / PostgreSQL] database
- Displays results as a table in the Streamlit interface


## Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **LLM:** Google Gemini API
- **Database:** [SQLite / MySQL / PostgreSQL]
- **Libraries:** `google-generativeai`, `streamlit`, `pandas`, `python-dotenv`

## How It Works

1. The user types a question, e.g. *"Show the top 5 customers by total sales"*.
2. The question and the database schema are sent to Gemini in a prompt.
3. Gemini returns a SQL query.
4. The query runs on the database and the results appear in the app.

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/saivenkatboora987-prog/[repo-name].git
cd [repo-name]
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
Get a free key from [Google AI Studio](https://aistudio.google.com/) and create a `.env` file:
```
GOOGLE_API_KEY=your_api_key_here
```
Never commit this file to GitHub.

### 4. Run the app
```bash
streamlit run app.py
```

## Example Questions

- "How many records are in the table?"
- "List all employees in the Data Science department"
- "What is the average salary by department?"

## Project Structure

```
├── app.py              # Streamlit application
├── [notebook].ipynb    # Experiments / development notebook
├── [database].db       # Sample database
├── requirements.txt
└── README.md
```

## Limitations and Future Work

- Add support for multiple databases
- Add query validation to block unsafe operations (DROP, DELETE)
- Add chat history and query explanations

## Author

**Boora Sai Venkat**
[LinkedIn](https://www.linkedin.com/in/boora-sai-venkat-771090367) | [GitHub](https://github.com/saivenkatboora987-prog)
