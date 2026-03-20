CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL
);

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NOT NULL,
    user_agent VARCHAR(255) NOT NULL,
    success BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_user_id ON audit_logs(user_id);
CREATE INDEX idx_login_time ON audit_logs(login_time);
CREATE INDEX idx_ip_address ON audit_logs(ip_address);
CREATE INDEX idx_user_agent ON audit_logs(user_agent);
CREATE INDEX idx_success ON audit_logs(success);