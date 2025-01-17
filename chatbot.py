import psycopg2
import re
import questionary

# Function to connect to PostgreSQL
def connect_to_postgres():
    host = questionary.text("Enter your PostgreSQL host (e.g., localhost):").ask()
    port = questionary.text("Enter your PostgreSQL port (default 5432):").ask()
    db_name = questionary.text("Enter your PostgreSQL database name:").ask()
    user = questionary.text("Enter your PostgreSQL username:").ask()
    password = questionary.password("Enter your PostgreSQL password:").ask()

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=db_name,
            user=user,
            password=password
        )
        print("Connected to PostgreSQL database successfully.")
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        exit()

# Function to query the database
def query_database(query, conn):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        return str(e)

# Chatbot logic
def process_user_input(user_input, conn):
    user_input = user_input.lower()

    if "missing accounts" in user_input:
        # Extract date range if mentioned
        date_match = re.search(r'from (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})', user_input)
        if date_match:
            start_date, end_date = date_match.groups()
            query = f"""
                SELECT account_id 
                FROM accounts 
                WHERE status = 'missing' AND created_at BETWEEN '{start_date}' AND '{end_date}'
            """
        else:
            query = "SELECT account_id FROM accounts WHERE status = 'missing'"
        
        results = query_database(query, conn)
        return f"Missing accounts: {results}" if results else "No missing accounts found."

    elif "active accounts" in user_input:
        query = "SELECT account_id FROM accounts WHERE status = 'active'"
        results = query_database(query, conn)
        return f"Active accounts: {results}" if results else "No active accounts found."

    else:
        return "Sorry, I didn't understand your query. Try asking about 'missing accounts' or 'active accounts'."

# Main chatbot function
def chatbot():
    conn = connect_to_postgres()
    print("Chatbot is ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        response = process_user_input(user_input, conn)
        print(f"Chatbot: {response}")

    conn.close()

# Run the chatbot
if __name__ == "__main__":
    chatbot()
