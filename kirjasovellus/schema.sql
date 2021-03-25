CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE books (id SERIAL PRIMARY KEY, title TEXT, author TEXT, genre TEXT, isbn TEXT UNIQUE, pages INTEGER);