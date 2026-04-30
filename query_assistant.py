import os

import mysql.connector as ms
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama


SCHEMA_DESCRIPTION = """
Database: customers
Table: customers
Columns:
- customer_id INT PRIMARY KEY
- first_name VARCHAR(50)
- last_name VARCHAR(50)
- email VARCHAR(100)
- phone VARCHAR(15)
- address VARCHAR(255)
- city VARCHAR(50)
- join_date DATE
"""

DATA_ANALYST_TEMPLATE = """
You are a careful data analyst.

Convert the user's request into a single read-only MySQL SELECT query.

Rules:
- Only output SQL.
- Do not explain the query.
- Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, or CREATE statements.
- Use only this schema:
{schema}

User request: {prompt}
"""


def get_db_config():
    return {
        "host": os.environ.get("MYSQL_HOST", "localhost"),
        "user": os.environ.get("MYSQL_USER", "root"),
        "password": os.environ.get("MYSQL_PASSWORD", ""),
        "database": os.environ.get("MYSQL_DATABASE", "customers"),
    }


def build_chain():
    prompt_template = PromptTemplate(
        input_variables=["schema", "prompt"],
        template=DATA_ANALYST_TEMPLATE,
    )
    llm = Ollama(model=os.environ.get("OLLAMA_MODEL", "gemma"))
    return LLMChain(llm=llm, prompt=prompt_template)


def extract_sql_code(input_string):
    sql = input_string.strip().strip("`")
    if sql.lower().startswith("sql"):
        sql = sql[3:].strip()
    return sql.rstrip(";")


def is_safe_select(sql_query):
    normalized = sql_query.strip().lower()
    blocked = ("insert", "update", "delete", "drop", "alter", "truncate", "create")
    return normalized.startswith("select") and not any(token in normalized for token in blocked)


def query_db(sql_query):
    if not is_safe_select(sql_query):
        raise ValueError("Only read-only SELECT queries are allowed.")

    con = ms.connect(**get_db_config())
    cursor = con.cursor()
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description or []]
        return columns, rows
    finally:
        cursor.close()
        con.close()

