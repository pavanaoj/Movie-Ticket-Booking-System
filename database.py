import sqlite3


def create_database():
    connection = sqlite3.connect("movie_booking.db")
    cursor = connection.cursor()

    # Movies table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_name TEXT NOT NULL,
            genre TEXT,
            duration INTEGER,
            language TEXT
        )
    """)

    # Shows table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shows (
            show_id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER,
            show_date TEXT,
            show_time TEXT,
            screen_no INTEGER,
            ticket_price REAL,
            FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
        )
    """)

    # Bookings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_phone TEXT,
            show_id INTEGER,
            seat_no TEXT,
            booking_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (show_id) REFERENCES shows(show_id),
            UNIQUE(show_id, seat_no)
        )
    """)

    # Add sample movies
    cursor.execute("SELECT COUNT(*) FROM movies")

    if cursor.fetchone()[0] == 0:
        movies = [
            ("Leo", "Action", 164, "Tamil"),
            ("Interstellar", "Science Fiction", 169, "English"),
            ("Jailer", "Action", 168, "Tamil"),
            ("Avatar", "Science Fiction", 162, "English")
        ]

        cursor.executemany("""
            INSERT INTO movies
            (movie_name, genre, duration, language)
            VALUES (?, ?, ?, ?)
        """, movies)

    # Add sample shows
    cursor.execute("SELECT COUNT(*) FROM shows")

    if cursor.fetchone()[0] == 0:
        shows = [
            (1, "2026-09-15", "10:00 AM", 1, 150),
            (1, "2026-09-15", "06:00 PM", 1, 180),
            (2, "2026-09-15", "02:00 PM", 2, 200),
            (3, "2026-09-16", "06:30 PM", 3, 150),
            (4, "2026-09-16", "09:00 PM", 2, 220)
        ]

        cursor.executemany("""
            INSERT INTO shows
            (movie_id, show_date, show_time, screen_no, ticket_price)
            VALUES (?, ?, ?, ?, ?)
        """, shows)

    connection.commit()
    connection.close()

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()
