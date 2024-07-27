import streamlit as st
import sqlite3  
import google.generativeai as genai
import os

# Load environment variables (replace with your actual API key)
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def execute_query(sql, db_file="STUDENT.db"):
    """Executes a provided SQL query on the specified database file."""
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        return data
    except sqlite3.Error as e:
        st.error(f"Error executing query: {e}")
        return None

def display_data(data):
    """Displays fetched data from the database in a Streamlit table."""
    if data:
        st.dataframe(data)
    else:
        st.write("No results found.")

st.title("SQL Query Generator and Executor (LLM)")

# Example prompt for the LLM model
prompt = [
    """You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION 

    For example,
    Example 1: How many entries of records are present?
    The SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;

    Example 2: Tell me all the students studying in Data Science class?
    The SQL command will be something like this: SELECT * FROM STUDENT where CLASS="Data Science";

    **Please ensure the generated SQL does not contain leading/trailing `sql` or backticks.**
    """
]

user_sentence = st.text_input("Enter your request in English:", key="sentence")
run_query = st.button("Run Query")

if run_query:
    if user_sentence:
        # Generate SQL query using GenAI model
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([prompt[0], user_sentence])
        generated_sql = response.text.strip()

        # Remove unnecessary characters
        generated_sql = generated_sql.replace("`", "").replace("`sql", "").replace("`", "")
        st.write("Generated SQL:", generated_sql)  # Show generated SQL for debugging

        # Execute the generated SQL query
        results = execute_query(generated_sql)
        display_data(results)
    else:
        st.warning("Please enter your request in English first.")
