CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE savings_goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    target_amount NUMERIC(10, 2) NOT NULL,
    current_amount NUMERIC(10, 2) DEFAULT 0.0,
    description TEXT
);

CREATE TABLE milestones (
    id SERIAL PRIMARY KEY,
    savings_goal_id INTEGER NOT NULL REFERENCES savings_goals(id),
    name VARCHAR(100) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    description TEXT
);

CREATE INDEX idx_savings_goals_user_id ON savings_goals(user_id);
CREATE INDEX idx_milestones_savings_goal_id ON milestones(savings_goal_id);