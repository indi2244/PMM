import pyodbc
import json
import sys

# Replace with your actual SQL Server credentials and configuration
server = 'localhost'
database = 'webapp'
username = 'indira'
password = 'mypassword'

# Establish connection


try:
    with open('users.json') as f:
        file_content = f.read()
        print("File Content:")
        print(file_content)
except FileNotFoundError:
    print("Error: users.json file not found.", file=sys.stderr)
    sys.exit(1)
    
try:
    conn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={'indii'};DATABASE={'webapp'};UID={'indira'};PWD={'mypassword'}")
    cursor = conn.cursor()
except pyodbc.Error as e:
    print(f"Error connecting to SQL Server: {e}", file=sys.stderr)
    sys.exit(1)



# Read JSON file
try:
    with open('users.json', encoding='utf-16') as f:
        users_data = json.load(f)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON format in users.json - {e}", file=sys.stderr)
    sys.exit(1)
except FileNotFoundError:
    print("Error: users.json file not found.", file=sys.stderr)
    sys.exit(1)

# Insert each user into MS SQL Server
try:
    for user_data in users_data:
        username = user_data['fields']['username']
        password = user_data['fields']['password']
        cursor.execute("INSERT INTO dbo.[User] (username, password) VALUES (?, ?)", username, password)
except pyodbc.Error as e:
    print(f"Error executing SQL query: {e}", file=sys.stderr)
    conn.rollback()
    sys.exit(1)
else:
    conn.commit()
    print("Data imported successfully.")
finally:
    conn.close()
