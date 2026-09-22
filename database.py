import sqlite3

DATABASE_NAME = "makerspace.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create database tables and sample data on first run."""
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'inactive'))
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                equipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'available'
                    CHECK (status IN ('available', 'borrowed', 'maintenance'))
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                equipment_id INTEGER NOT NULL,
                checkout_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                return_date TEXT,
                status TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'returned')),
                FOREIGN KEY (member_id) REFERENCES members(member_id),
                FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
            )
        """)

        # Add simple sample data only when the database is completely empty.
        member_count = cursor.execute(
            "SELECT COUNT(*) FROM members"
        ).fetchone()[0]

        if member_count == 0:
            cursor.execute("""
                INSERT INTO members (name, email, phone)
                VALUES (?, ?, ?)
            """, ("Ada Lovelace", "ada@example.com", "555-0101"))

            cursor.execute("""
                INSERT INTO members (name, email, phone)
                VALUES (?, ?, ?)
            """, ("Alan Turing", "alan@example.com", "555-0102"))

        equipment_count = cursor.execute(
            "SELECT COUNT(*) FROM equipment"
        ).fetchone()[0]

        if equipment_count == 0:
            cursor.execute("""
                INSERT INTO equipment (name, category, status)
                VALUES (?, ?, ?)
            """, ("Soldering Kit", "Electronics", "available"))

            cursor.execute("""
                INSERT INTO equipment (name, category, status)
                VALUES (?, ?, ?)
            """, ("Digital Camera", "Photography", "available"))

            cursor.execute("""
                INSERT INTO equipment (name, category, status)
                VALUES (?, ?, ?)
            """, ("3D Printer Nozzle Set", "3D Printing", "available"))

        connection.commit()


def fetch_all(query, parameters=()):
    """Run a SELECT query and return all rows."""
    with get_connection() as connection:
        cursor = connection.execute(query, parameters)
        return cursor.fetchall()


def fetch_one(query, parameters=()):
    """Run a SELECT query and return one row."""
    with get_connection() as connection:
        cursor = connection.execute(query, parameters)
        return cursor.fetchone()


def execute_query(query, parameters=()):
    """Run an INSERT, UPDATE or DELETE query."""
    with get_connection() as connection:
        cursor = connection.execute(query, parameters)
        connection.commit()
        return cursor.lastrowid, cursor.rowcount
