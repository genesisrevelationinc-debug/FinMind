CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE savings_goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    target_amount FLOAT NOT NULL,
    current_amount FLOAT DEFAULT 0.0,
    description VARCHAR(255)
);

CREATE TABLE milestones (
    id SERIAL PRIMARY KEY,
    savings_goal_id INTEGER NOT NULL REFERENCES savings_goals(id),
    name VARCHAR(100) NOT NULL,
    amount FLOAT NOT NULL,
    description VARCHAR(255)
);

CREATE INDEX idx_user_savings_goals ON savings_goals(user_id);
CREATE INDEX idx_savings_goal_milestones ON milestones(savings_goal_id);