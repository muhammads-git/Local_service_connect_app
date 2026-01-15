import mysql.connector
import os
import time
from mysql.connector import Error

def runMigrations():
    db_config = {
    'host': os.getenv('DB_HOST', 'switchyard.proxy.rlwy.net'), 
    'user': os.getenv('DB_USER', 'root'),
    'port':  int(os.getenv('DB_PORT', 49423)),   # ← ADD _ 
    'password': os.getenv('DB_PASSWORD', 'JkBFoZOTIMdAUzpoXhsbrftfHyHmasvX'),  # ← ADD _
    'database': os.getenv('DB_NAME', 'railway'),  # ← ADD _
    'connection_timeout': 30
    }
    
    attempts = 0
    max_attempts = 5
    db = None
    
    while attempts < max_attempts:
        try:
            print(f"Attempting to connect (Attempt {attempts + 1}/{max_attempts})...")
            db = mysql.connector.connect(**db_config)   
            if db.is_connected():
                print("Connection successful!")
                break  # Exit the loop on success
        except Error as e:
            print(f"Connection failed: {e}")

            attempts += 1
            if attempts == max_attempts:
                print("Max retries reached. Please check if your Railway database is awake.")
                return
            print(f"Retrying in 5 seconds...")
            time.sleep(5)  # Wait before retrying
    
    cursor = db.cursor()

    # Get all migrations files
    migrationFolder = "database/migrations/"
    migrationsFiles = sorted(os.listdir(migrationFolder))


    # Check which migrations run already
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS migrations_history(
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   filename VARCHAR(255),
                   applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )            
                """)
    # Get already applied migration
    cursor.execute(" SELECT filename FROM migrations_history ")
    all = cursor.fetchall()
    applied = [ row[0] for row in cursor.fetchall() ]

    # Run new migrations
    for filename in migrationsFiles:
        if filename.endswith(".sql") and filename not in applied:
            print(f"Running: {filename}")

            # Read SQL file
            with open(os.path.join(migrationFolder,filename), 'r') as f:
                sql = f.read()
    

            # Run sql commands
            for statement in sql.split(';'):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except Error as e:
                        print(f"Error executing statement: {e}")
                        print(f"Problem statement: {statement[:100]}...")
            
            # Mark as applied - FIXED SYNTAX
            cursor.execute("INSERT INTO migrations_history (filename) VALUES(%s)", (filename,))
            print(f"Applied: {filename}")
    
    # Commit changes
    db.commit()
    cursor.close()
    db.close()

    print("All migrations complete!")

if __name__ == "__main__":
    runMigrations()