CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL
);

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    name VARCHAR(150) NOT NULL,
    balance NUMERIC NOT NULL
);

CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    category VARCHAR(150) NOT NULL,
    notes TEXT,
    date DATE NOT NULL,
    account_id INTEGER REFERENCES accounts(id) ON DELETE SET NULL
);

CREATE TABLE bills (
    cadence VARCHAR(50) NOT NULL,
    due_date DATE NOT NULL,
    channel VARCHAR(50),
    account_id INTEGER REFERENCES accounts(id) ON DELETE SET NULL
);

CREATE TABLE reminders (