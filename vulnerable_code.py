import sqlite3

def fetch_user_profile(user_input):
    """
    Connects to the database and fetches a user's profile based on their username.
    """
    # DANGER: Directly injecting user input into the SQL string using an f-string
    query = f"SELECT id, email, role FROM users WHERE username = '{user_input}'"
    
    try:
        # Simulated database connection
        connection = sqlite3.connect('company_database.db')
        cursor = connection.cursor()
        
        # Executing the vulnerable query
        cursor.execute(query)
        user_data = cursor.fetchall()
        
        connection.close()
        return user_data
        
    except sqlite3.Error as error:
        print("Failed to read data from database", error)
        return None