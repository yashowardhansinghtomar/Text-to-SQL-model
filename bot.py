from query_assistant import SCHEMA_DESCRIPTION, build_chain, extract_sql_code, query_db


def main():
    chain = build_chain()
    while True:
        user_input = input("Question (or 'exit'): ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        result = chain.run(schema=SCHEMA_DESCRIPTION, prompt=user_input)
        sql_query = extract_sql_code(result)
        print(f"\nSQL: {sql_query}\n")

        try:
            columns, rows = query_db(sql_query)
            print(columns)
            for row in rows:
                print(row)
        except Exception as exc:
            print(f"Query failed: {exc}")


if __name__ == "__main__":
    main()
