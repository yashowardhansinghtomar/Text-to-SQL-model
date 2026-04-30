# Text to SQL Model

A Streamlit prototype that converts natural-language questions into SQL for a local MySQL `customers` database using an Ollama-hosted LLM.

## What It Shows

- Prompt engineering for constrained SQL generation
- Local LLM usage through Ollama and LangChain
- Streamlit UI for natural-language database querying
- Basic safety guardrails for read-only `SELECT` queries
- MySQL connection configuration through environment variables

## Expected Database

Database: `customers`

Table: `customers`

| Column | Type |
| --- | --- |
| `customer_id` | `INT PRIMARY KEY` |
| `first_name` | `VARCHAR(50)` |
| `last_name` | `VARCHAR(50)` |
| `email` | `VARCHAR(100)` |
| `phone` | `VARCHAR(15)` |
| `address` | `VARCHAR(255)` |
| `city` | `VARCHAR(50)` |
| `join_date` | `DATE` |

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run an Ollama model locally:

   ```bash
   ollama run gemma
   ```

3. Configure MySQL:

   ```powershell
   $env:MYSQL_HOST="localhost"
   $env:MYSQL_USER="root"
   $env:MYSQL_PASSWORD="your_password_here"
   $env:MYSQL_DATABASE="customers"
   $env:OLLAMA_MODEL="gemma"
   ```

4. Start the app:

```bash
streamlit run app.py
```

Or run the terminal version:

```bash
python bot.py
```

## Safety Notes

This prototype only executes generated SQL that starts with `SELECT`. It blocks destructive statements such as `DROP`, `DELETE`, `UPDATE`, and `INSERT`.

For production use, add schema introspection, query validation, row limits, logging, and database permissions restricted to read-only access.
