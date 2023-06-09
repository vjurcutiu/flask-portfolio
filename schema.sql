DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE video (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username_id TEXT NOT NULL,
  video TEXT UNIQUE,
  FOREIGN KEY (username_id) REFERENCES user (id)
);
