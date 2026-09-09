CREATE DATABASE movie_ticket_booking;

USE movie_ticket_booking;

-- Movies table
CREATE TABLE movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_name VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    duration INT,
    language VARCHAR(30)
);

-- Shows table
CREATE TABLE shows (
    show_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    show_date DATE,
    show_time TIME,
    screen_no INT,
    ticket_price DECIMAL(10,2),
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
);

-- Bookings table
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(15),
    show_id INT,
    seat_no VARCHAR(10),
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (show_id) REFERENCES shows(show_id)
);

-- Sample movies
INSERT INTO movies (movie_name, genre, duration, language)
VALUES
('Leo', 'Action', 164, 'Tamil'),
('Interstellar', 'Science Fiction', 169, 'English'),
('Jailer', 'Action', 168, 'Tamil'),
('Avatar', 'Science Fiction', 162, 'English');

-- Sample shows
INSERT INTO shows
(movie_id, show_date, show_time, screen_no, ticket_price)
VALUES
(1, '2026-09-15', '10:00:00', 1, 150.00),
(1, '2026-09-15', '18:00:00', 1, 180.00),
(2, '2026-09-15', '14:00:00', 2, 200.00),
(3, '2026-09-16', '18:30:00', 3, 150.00),
(4, '2026-09-16', '21:00:00', 2, 220.00);
