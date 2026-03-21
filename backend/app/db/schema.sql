CREATE TABLE savings_goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    goal_name VARCHAR(255) NOT NULL,
    target_amount NUMERIC NOT NULL,
    current_amount NUMERIC DEFAULT 0.0,
    start_date DATE DEFAULT CURRENT_DATE,
    end_date DATE
);

CREATE TABLE milestones (
    id SERIAL PRIMARY KEY,
    savings_goal_id INTEGER NOT NULL REFERENCES savings_goals(id),
    milestone_name VARCHAR(255) NOT NULL,
    amount NUMERIC NOT NULL,
    achieved BOOLEAN DEFAULT FALSE
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,