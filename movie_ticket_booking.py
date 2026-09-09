import mysql.connector


# Connect to MySQL
def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="movie_ticket_booking"
    )


# Display movies
def view_movies():
    db = connect_database()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM movies")

    movies = cursor.fetchall()

    print("\n========== AVAILABLE MOVIES ==========")

    for movie in movies:
        print(
            f"ID: {movie[0]} | "
            f"Movie: {movie[1]} | "
            f"Genre: {movie[2]} | "
            f"Duration: {movie[3]} min | "
            f"Language: {movie[4]}"
        )

    cursor.close()
    db.close()


# Display shows
def view_shows():
    db = connect_database()
    cursor = db.cursor()

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

    cursor.close()
    db.close()


# Book ticket
def book_ticket():
    db = connect_database()
    cursor = db.cursor()

    view_shows()

    show_id = int(input("\nEnter Show ID: "))
    seat_no = input("Enter Seat Number (Example A1): ").upper()
    customer_name = input("Enter Customer Name: ")
    customer_phone = input("Enter Phone Number: ")

    # Check whether seat is already booked
    check_query = """
    SELECT * FROM bookings
    WHERE show_id = %s AND seat_no = %s
    """

    cursor.execute(check_query, (show_id, seat_no))

    if cursor.fetchone():
        print("\n❌ This seat is already booked.")
    else:
        insert_query = """
        INSERT INTO bookings
        (customer_name, customer_phone, show_id, seat_no)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (customer_name, customer_phone, show_id, seat_no)
        )

        db.commit()

        print("\n✅ Ticket booked successfully!")
        print("Booking ID:", cursor.lastrowid)

    cursor.close()
    db.close()


# View bookings
def view_bookings():
    db = connect_database()
    cursor = db.cursor()

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

    print("\n========== BOOKINGS ==========")

    if not bookings:
        print("No bookings found.")

    for booking in bookings:
        print(
            f"Booking ID: {booking[0]} | "
            f"Name: {booking[1]} | "
            f"Phone: {booking[2]} | "
            f"Movie: {booking[3]} | "
            f"Date: {booking[4]} | "
            f"Time: {booking[5]} | "
            f"Seat: {booking[6]}"
        )

    cursor.close()
    db.close()


# Cancel booking
def cancel_booking():
    db = connect_database()
    cursor = db.cursor()

    booking_id = int(input("\nEnter Booking ID to cancel: "))

    query = "DELETE FROM bookings WHERE booking_id = %s"

    cursor.execute(query, (booking_id,))

    if cursor.rowcount > 0:
        db.commit()
        print("\n✅ Booking cancelled successfully.")
    else:
        print("\n❌ Booking ID not found.")

    cursor.close()
    db.close()


# Main menu
def main():
    while True:

        print("\n")
        print("====================================")
        print("     🎬 MOVIE TICKET BOOKING SYSTEM")
        print("====================================")
        print("1. View Movies")
        print("2. View Shows")
        print("3. Book Ticket")
        print("4. View Bookings")
        print("5. Cancel Booking")
        print("6. Exit")
        print("====================================")

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
            print("\nThank you for using Movie Ticket Booking System!")
            break

        else:
            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
