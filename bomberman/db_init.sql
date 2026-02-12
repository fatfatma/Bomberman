CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE game_stats (
  stat_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  wins INT DEFAULT 0,
  losses INT DEFAULT 0,
  total_games INT DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE leaderboard (
  score_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  score INT NOT NULL,
  game_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE user_preferences (
  pref_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  theme VARCHAR(50) DEFAULT 'desert',
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);
