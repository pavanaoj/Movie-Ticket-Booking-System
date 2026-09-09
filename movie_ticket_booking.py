import sqlite3


DATABASE = "movie_booking.db"


def connect_database():
    return sqlite3.connect(DATABASE)


# -----------------------------
# VIEW MOVIES
# -----------------------------
def view_movies():

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM movies")

    movies = cursor.fetchall()

    print("\n========== AVAILABLE MOVIES ==========")

    for movie in movies:
        print(
            f"ID: {movie[0]} | "
            f"{movie[1]} | "
            f"Genre: {movie[2]} | "
            f"Duration: {movie[3]} min | "
            f"Language: {movie[4]}"
        )

    connection.close()


# -----------------------------
# VIEW SHOWS
# -----------------------------
def view_shows():

    connection = connect_database()
    cursor = connection.cursor()

    query = """
        SELECT shows.show_id,
               movies.movie_name,
               shows.show_date,
               shows.show_time,
               shows.screen_no,
               shows.ticket_price
        FROM shows
        JOIN movies
        ON shows.movie_id = movies.movie_id
    """

    cursor.execute(query)

    shows = cursor.fetchall()

    print("\n========== AVAILABLE SHOWS ==========")

    for show in shows:
        print(
            f"Show ID: {show[0]} | "
            f"Movie: {show[1]} | "
            f"Date: {show[2]} | "
            f"Time: {show[3]} | "
            f"Screen: {show[4]} | "
            f"Price: ₹{show[5]}"
        )

    connection.close()


# -----------------------------
# BOOK TICKET
# -----------------------------
def book_ticket():

    connection = connect_database()
    cursor = connection.cursor()

    view_shows()

    try:
        show_id = int(input("\nEnter Show ID: "))
    except ValueError:
        print("Invalid Show ID.")
        connection.close()
        return

    seat_no = input("Enter Seat Number (Example A1): ").upper()
    customer_name = input("Enter Customer Name: ")
    customer_phone = input("Enter Phone Number: ")

    try:

        query = """
            INSERT INTO bookings
            (customer_name, customer_phone, show_id, seat_no)
            VALUES (?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (customer_name, customer_phone, show_id, seat_no)
        )

        connection.commit()

        booking_id = cursor.lastrowid

        print("\n✅ TICKET BOOKED SUCCESSFULLY!")
        print("--------------------------------")
        print("Booking ID :", booking_id)
        print("Customer   :", customer_name)
        print("Seat       :", seat_no)
        print("--------------------------------")

    except sqlite3.IntegrityError:

        print("\n❌ This seat is already booked.")

    connection.close()


# -----------------------------
# VIEW BOOKINGS
# -----------------------------
def view_bookings():

    connection = connect_database()
    cursor = connection.cursor()

    query = """
        SELECT bookings.booking_id,
               bookings.customer_name,
               bookings.customer_phone,
               movies.movie_name,
               shows.show_date,
               shows.show_time,
               bookings.seat_no
        FROM bookings
        JOIN shows
        ON bookings.show_id = shows.show_id
        JOIN movies
        ON shows.movie_id = movies.movie_id
    """

    cursor.execute(query)

    bookings = cursor.fetchall()

    print("\n========== ALL BOOKINGS ==========")

    if not bookings:
        print("No bookings found.")

    for booking in bookings:
        print(
            f"Booking ID: {booking[0]} | "
            f"Name: {booking[1]} | "
            f"Movie: {booking[3]} | "
            f"Date: {booking[4]} | "
            f"Time: {booking[5]} | "
            f"Seat: {booking[6]}"
        )

    connection.close()


# -----------------------------
# CANCEL BOOKING
# -----------------------------
def cancel_booking():

    connection = connect_database()
    cursor = connection.cursor()

    try:
        booking_id = int(input("\nEnter Booking ID: "))
    except ValueError:
        print("Invalid Booking ID.")
        connection.close()
        return

    cursor.execute(
        "DELETE FROM bookings WHERE booking_id = ?",
        (booking_id,)
    )

    if cursor.rowcount > 0:
        connection.commit()
        print("\n✅ Booking cancelled successfully.")
    else:
        print("\n❌ Booking ID not found.")

    connection.close()


# -----------------------------
# MAIN MENU
# -----------------------------
def main():

    while True:

        print("\n")
        print("========================================")
        print("       🎬 MOVIE TICKET BOOKING")
        print("========================================")
        print("1. View Movies")
        print("2. View Shows")
        print("3. Book Ticket")
        print("4. View Bookings")
        print("5. Cancel Booking")
        print("6. Exit")
        print("========================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_movies()

        elif choice == "2":
            view_shows()

        elif choice == "3":
            book_ticket()

        elif choice == "4":
            view_bookings()

        elif choice == "5":
            cancel_booking()

        elif choice == "6":
            print("\nThank you for using the system! 🎬")
            break

        else:
            print("\n❌ Invalid choice.")


if __name__ == "__main__":
    main()
