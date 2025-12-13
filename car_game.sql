CREATE DATABASE car_game;

USE car_game;

CREATE TABLE leaderboard (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    score INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM leaderboard ORDER BY score DESC LIMIT 5;

USE car_game;

DELETE FROM leaderboard WHERE id < 26;