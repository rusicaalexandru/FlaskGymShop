DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS subscription;
DROP TABLE IF EXISTS plan;
DROP TABLE IF EXISTS role;

CREATE TABLE role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Populate the role table with predefined roles
INSERT INTO role (name) VALUES ('guest'), ('user'), ('admin');

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nickname TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role (id)
);

CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    image_path TEXT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE subscription (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (plan_id) REFERENCES plan (id)
);

CREATE TABLE plan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    duration INTEGER NOT NULL,
    description TEXT
);

CREATE TABLE cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (post_id) REFERENCES post (id)
);

INSERT INTO user (username, password, created, nickname, role_id)
VALUES
('admin', 'scrypt:32768:8:1$ufggR0XSoDHzvzjV$1e3d0dda1dd0f0fb1d2ff6062ce94507f81a605a3426590c1c91edd5dd7c11e0c244a9ff0c6137f4e6a877426a6b03ec94fea026f52ceac0345f1d3d590d4326', CURRENT_TIMESTAMP, 'AdminUser', (SELECT id FROM role WHERE name='admin')),
('user1', 'scrypt:32768:8:1$1bVU5CV1UkgiHBzw$1c17317fbf87f5f4f3bf79f48fb33be08bcd41ea630ed1dbc495919d7f667f2443204c6cc6bd10d3d971277eff693081af9fbd719500463c996650b33dc5a5bc', CURRENT_TIMESTAMP, 'UserOne', (SELECT id FROM role WHERE name='user')),
('user2', 'scrypt:32768:8:1$yE3ATopbZsNnJ8Uk$60f4a6d6ca2846a9aa92832c08c712e4fed4d6e2d6cf474d7f5ef0f4fadbbc5bff00a60db6867a47b6768429b66741d8dec86558cc5728fd0505a8426eb53659', CURRENT_TIMESTAMP, 'UserTwo', (SELECT id FROM role WHERE name='user'));