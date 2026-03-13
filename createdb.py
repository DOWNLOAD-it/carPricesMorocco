import pandas as pd
import sqlite3

# Load the CSV file
file_path = "cars.csv"  # Make sure to replace this with the correct file path
df = pd.read_csv(file_path)

# Clean up column names by stripping leading/trailing spaces
df.columns = df.columns.str.strip()

# Print the column names to inspect them
print("Columns in CSV:", df.columns)

# Check for required columns
required_columns = ["Marque", "Modele", "Ville", "Secteur"]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    print(f"Missing columns: {missing_columns}")
else:
    print("All required columns are present.")

    # Proceed with data processing and database insertion
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    # Create tables for storing data
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Marque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Modele (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marque_id INTEGER,
        name TEXT NOT NULL,
        FOREIGN KEY (marque_id) REFERENCES Marque(id)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Ville (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Secteur (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ville_id INTEGER,
        name TEXT NOT NULL,
        FOREIGN KEY (ville_id) REFERENCES Ville(id)
    );
    """
    )

    # Insert data into Marque and Modele
    for marque in df["Marque"].unique():
        cursor.execute("INSERT OR IGNORE INTO Marque (name) VALUES (?)", (marque,))
        conn.commit()  # Commit after each insert to avoid large memory usage

    for marque in df["Marque"].unique():
        marque_id = cursor.execute(
            "SELECT id FROM Marque WHERE name = ?", (marque,)
        ).fetchone()[0]

        # Insert modele for each marque
        for modele in df[df["Marque"] == marque]["Modele"].unique():
            cursor.execute(
                "INSERT OR IGNORE INTO Modele (marque_id, name) VALUES (?, ?)",
                (marque_id, modele),
            )
        conn.commit()

    # Insert data into Ville and Secteur
    for ville in df["Ville"].unique():
        cursor.execute("INSERT OR IGNORE INTO Ville (name) VALUES (?)", (ville,))
        conn.commit()

    for ville in df["Ville"].unique():
        # Check if the ville exists in the Ville table
        result = cursor.execute(
            "SELECT id FROM Ville WHERE name = ?", (ville,)
        ).fetchone()

        if result:  # If result is not None
            ville_id = result[0]
            # Insert secteur for each ville
            for secteur in df[df["Ville"] == ville]["Secteur"].unique():
                cursor.execute(
                    "INSERT OR IGNORE INTO Secteur (ville_id, name) VALUES (?, ?)",
                    (ville_id, secteur),
                )
            conn.commit()
        else:
            print(f"Error: Ville '{ville}' not found in the database.")

    # Close the SQLite connection
    conn.close()

    print("Data has been inserted into the database successfully!")
