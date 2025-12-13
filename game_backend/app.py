import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to MySQL
db = pymysql.connect(
    host="localhost",
    user="root",
    password="XXXXXX",
    database="car_game",
    cursorclass=pymysql.cursors.DictCursor
)

@app.route("/submit", methods=["POST"])
def submit_score():
    data = request.get_json()
    name = data.get("name")
    score = data.get("score")

    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO leaderboard (name, score) VALUES (%s, %s)",
            (name, score)
        )
        db.commit()

    return jsonify({"status": "success"}), 201

@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    with db.cursor() as cur:
        cur.execute(
            "SELECT name, score FROM leaderboard ORDER BY score DESC LIMIT 5"
        )
        results = cur.fetchall()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
