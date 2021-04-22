CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);
CREATE TABLE books (id SERIAL PRIMARY KEY, title TEXT, author TEXT, genre TEXT, isbn TEXT UNIQUE, pages INTEGER);
CREATE TABLE bookshelf_books (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users ON DELETE CASCADE, book_id INTEGER REFERENCES books ON DELETE CASCADE, progress INTEGER, update_date TIMESTAMP);
CREATE TABLE ratings (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, book_id INTEGER REFERENCES books, star_rating INTEGER, review TEXT, rating_date TIMESTAMP);
CREATE TYPE friend_status AS ENUM('sent', 'waiting', 'ok');
CREATE TABLE friends (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, friend_id INTEGER, friend_status friend_status);