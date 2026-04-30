import streamlit as st
from query_assistant import SCHEMA_DESCRIPTION, build_chain, extract_sql_code, query_db


st.title("Text to SQL Query Assistant")
st.caption("Ask questions about the local MySQL customers table.")

user_input = st.text_input("Question", placeholder="Show customers from Mumbai who joined this year")

if st.button("Generate and Run SQL"):
    if not user_input.strip():
        st.warning("Enter a question first.")
    else:
        with st.spinner("Generating SQL..."):
            chain = build_chain()
            result = chain.run(schema=SCHEMA_DESCRIPTION, prompt=user_input)
            sql_query = extract_sql_code(result)

        st.code(sql_query, language="sql")

        try:
            columns, rows = query_db(sql_query)
            st.dataframe([dict(zip(columns, row)) for row in rows])
        except Exception as exc:
            st.error(f"Query failed: {exc}")
