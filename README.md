# 🏎️ Multi-Vehicle Car Game & Leaderboard System

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-green?style=for-the-badge&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql)
![Pygame](https://img.shields.io/badge/Pygame-Frontend-red?style=for-the-badge&logo=pygame)

**A robust 2D infinite-runner car game built with Python (Pygame) featuring a full-stack leaderboard system using Flask and MySQL.**

## 📖 About The Project

This project is a complete software application that combines game development with web backend technologies. 

* **The Frontend** is a dynamic 2D game where players dodge traffic, manage fuel, and deal with changing weather conditions.
* **The Backend** is a REST API built with Flask that processes score submissions and serves a global leaderboard.
* **The Database** uses MySQL to persistently store player data.

Unlike simple standalone games, this project demonstrates **Client-Server Architecture** and **Asynchronous Networking** (threading) to ensure smooth gameplay while communicating with the server.

---

## 🎥 Live Demo

A complete video demonstration of the application, from user registration to submitting a service request, is available on YouTube. Click the thumbnail below to watch.

[<img src = "assets/new (1).jpg"/>](https://youtu.be/u3mVQ0xqKAM)

---

## 🚀 Key Features

### 🎮 Gameplay Mechanics
* **Infinite Scrolling:** Procedurally generated traffic and road environments.
* **Resource Management:** Fuel system requires players to collect fuel cans to survive.
* **Dynamic Weather:** Random weather cycles including **Rain**, **Snow**, **Fog**, and **Heat waves**.
* **Scoring System:**
    * ❤️ **Hearts:** Bonus points.
    * 🪙 **Coins:** Score multiplier.
    * 🔥 **Fire:** Penalty (deducts score).
* **Customization:** Select from 7 different car models and 12 different road environments.
* **Physics:** Jumping mechanic to avoid obstacles.

### ⚙️ Technical Features
* **Full-Stack Integration:** Connects Python game logic to a Web API.
* **Real-Time Leaderboard:** Displays top 5 scores fetched live from the database.
* **Non-Blocking Networking:** Uses Python `threading` to send HTTP requests without freezing the game loop.
* **Data Persistence:** MySQL database stores player names, scores, and timestamps.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | Python, Pygame | Game loop, rendering, and logic. |
| **Backend** | Flask (Python) | REST API to handle POST/GET requests. |
| **Database** | MySQL | Relational database for storing scores. |
| **Networking** | Requests, Threading | HTTP communication between game and server. |

---

## 💻 Installation & Setup

Follow these steps to run the project locally.

### 1. Prerequisites
* Python 3.x installed.
* MySQL Server installed and running.
* Git.

### 2. Clone the Repository
```bash```
```
git clone [https://github.com/Alphashivesh/Car_game.git](https://github.com/Alphashivesh/Car_game.git)
cd Car_game
```

### 3. Install Dependencies
```bash```
```
pip install -r requirements.txt
```

### 4. Database Setup
1. Open your MySQL client (Workbench or Command Line).
2. Create the database and table by running the SQL commands found in `leaderboard.sql` (or `car_game.sql`):
```sql```
```
CREATE DATABASE car_game;
USE car_game;
CREATE TABLE leaderboard (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    score INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Configure Backend
1. Open `game_backend/app.py`.
2. Update the database connection settings with **your** MySQL password:
```python```
```
db = pymysql.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD_HERE",  # <--- Update this!
    database="car_game"
)
```
---

## ▶️ How to Run

You need to run the backend and the game in separate terminals.

**Step 1: Start the Server**
Open a terminal:
```bash```
cd game_backend
python app.py

---

**Step 2: Launch the Game Open a new terminal window:**
Open a terminal:
```bash```
cd game_frontend
python main2.py

## 🕹️ Controls

| Key | Action |
| :--- | :--- |
| **Arrow Keys / WASD** | Move Car (Left, Right, Up, Down) |
| **Spacebar** | Jump (Avoid obstacles) |
| **P / Enter** | Pause Game |
| **M / Shift** | Mute Audio |
| **+ / -** | Adjust Volume |

---

## 📂 Project Structure

```
Car_game/
│
├── game_backend/
│   └── app.py              # Flask API server
│
├── game_frontend/
│   ├── main2.py            # Main game entry point
│   ├── file/               # Images (Cars, Roads, Obstacles)
│   └── sounds/             # Audio files (BGM, SFX)
│
├── leaderboard.sql         # SQL script for database setup
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```
---

## 📸 Snapshots

<table>
  <tr>
    <td align="center"><strong>Home Screen</strong></td>
    <td align="center"><strong>Instruction Screen</strong></td>
    <td align="center"><strong>Menu Screen</strong></td>
  </tr>
 
  <tr>
    <td><img src="assets/Screenshot 2025-12-13 202921.png" alt="Home Screen" width="250" height="500"/></td>
    <td><img src="assets/Screenshot 2025-12-13 203002.png" alt="Instruction Screen" width="250" height="500"/></td>
    <td><img src="assets/Screenshot 2025-12-13 203030.png" alt="Menu Screen" width="250" height="500"/></td>
  </tr> 
  <tr>
    <td align="center"><strong>Resumed Screen</strong></td>
    <td align="center"><strong>Name Submit Screen</strong></td>
    <td align="center"><strong>Game Over Screen</strong></td>
  </tr>
  <tr>
    <td><img src="assets/Screenshot 2025-12-13 220154.png" alt="Resume Screen" width="250" height="500"/></td>
    <td><img src="assets/Screenshot 2025-12-13 203050.png" alt="Name Submit Screen" width="250" height="500"/></td>
    <td><img src="assets/Screenshot 2025-12-13 203107.png" alt="Game Over Screen" width="250" height="500"/></td>
  </tr>
</table>

---

## 🔮 Future Improvements

- [ ] Add multiplayer support using WebSockets.
- [ ] Create a web-based frontend to view the leaderboard in a browser.
- [ ] Add user authentication (Login/Signup).
- [ ] Add difficulty settings menu.

---

## 👤 Author

**Alphashivesh**
- GitHub: [https://github.com/Alphashivesh](https://github.com/Alphashivesh)

---
*Created for the Hobby Project demonstrating Full Stack capabilities.*
