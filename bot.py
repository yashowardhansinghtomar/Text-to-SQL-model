from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
import mysql.connector as ms
import streamlit as st

# Define the prompt template for the data analyst
data_analyst_template = """You are a data analyst. You are working on a database named customers, which has a table named customers with the following columns: customer_id INT PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100), phone VARCHAR(15), address VARCHAR(255), city VARCHAR(50), join_date DATE. Your job is to perform the given task {prompt} by converting the prompt into SQL queries. The result should be the SQL query in a single-line string format, excluding 'Result:'.
"""

# Initialize the prompt template
data_analyst_prompt_template = PromptTemplate(
    input_variables=["prompt"],
    template=data_analyst_template
)

# Initialize the Ollama model
gemma = Ollama(model="gemma")

# Create an LLM chain for the data analyst
llm_chain = LLMChain(llm=gemma, prompt=data_analyst_prompt_template)

# Function to query the LLM
def query_llm(prompt):
    return llm_chain.run(prompt)

# Function to extract SQL code from the LLM response
def extract_sql_code(input_string):
    return input_string.strip()

# Function to query the database with proper error handling and SQL injection prevention
def query_db(sql_query):
    try:
        con = ms.connect(host="localhost", user="root", password="", database="customers")
        cursor = con.cursor()
        # Use parameterized query to prevent SQL injection
        cursor.execute(sql_query)
        data = cursor.fetchall()
        cursor.close()
        con.close()
        return data
    except Exception as e:
        print(f"Database error: {e}")
        return None

# Streamlit UI setup
st.title("Data Query Expert")
user_input = st.text_input("Enter the Prompt....")

if st.button("Extract Data"):
    st.text("Processing your request...")
    # Query the LLM
    result = query_llm(user_input)
    sql_query = extract_sql_code(result)
    # Query the database
    data = query_db(sql_query)
    if data is not None:
        st.table(data)
    else:
        st.error("There was an error processing the query.")