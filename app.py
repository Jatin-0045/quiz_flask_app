from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import random

app = Flask(__name__)
app.secret_key = "intelliquiz_secret_key"

# -------------------- DATABASE --------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="intelliquiz"
)

# -------------------- AUTH --------------------
@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        hashed = generate_password_hash(password)
        cur = db.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, hashed)
            )
            db.commit()
            flash("Account created successfully.", "success")
            return redirect(url_for("login"))
        except:
            flash("Username already exists.", "error")
        finally:
            cur.close()

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE TRIM(username)=%s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("index"))

        flash("Invalid username or password", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("welcome"))

# -------------------- QUIZ ENTRY --------------------
@app.route("/index", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        session["subject"] = request.form["subject"]
        session["difficulty"] = request.form["difficulty"].lower()
        return redirect(url_for("quiz"))

    return render_template("index.html")

@app.route("/quiz")
def quiz():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("quiz.html")

# -------------------- TOKEN --------------------
def get_token(reset=False):
    if reset or "trivia_token" not in session:
        r = requests.get("https://opentdb.com/api_token.php?command=request")
        session["trivia_token"] = r.json()["token"]
    return session["trivia_token"]

# -------------------- QUESTIONS --------------------
@app.route("/get-questions")
def get_questions():
    subject = session.get("subject")
    difficulty = session.get("difficulty", "easy")

    category_map = {
        "General Knowledge": 9,
        "Science & Nature": 17,
        "Computers": 18,
        "Mathematics": 19,
        "Sports": 21,
        "Geography": 22,
        "History": 23,
        "Politics": 24
    }

    ENTERTAINMENT_CATEGORIES = [
        10, # Books
        11, # Film
        12, # Music
        13, # Musicals & Theatre
        14, # Television
        15, # Video Games
        16, # Board Games
        29, # Comics
        31, # Anime & Manga
        32  # Cartoons & Animations
    ]

    if subject == "General Entertainment":
        category = random.choice(ENTERTAINMENT_CATEGORIES)
    else:
        category = category_map.get(subject, 9)

    token = get_token()

    params = {
        "amount": 10,
        "category": category,
        "difficulty": difficulty,
        "type": "multiple",
        "token": token
    }

    response = requests.get("https://opentdb.com/api.php", params=params)
    data = response.json()

    if data.get("response_code") == 4:
        token = get_token(reset=True)
        params["token"] = token
        data = requests.get("https://opentdb.com/api.php", params=params).json()

    return jsonify(data)

# -------------------- RESULT --------------------
@app.route("/result", methods=["POST"])
def result():
    score = int(request.form.get("score", 0))
    total = int(request.form.get("total", 0))
    percentage = (score / total) * 100 if total else 0

    if 0 < total < 10: 
        msg = ("🙂 Thanks for playing! You can jump back in anytime.")
    elif total == 0:
        msg = ("💙 Thanks for stopping by — see you again!")
    else:
        msg = (
            "🔥 Excellent! You have become a pro in this" if percentage == 100 else
            "💪 Good job! You are getting better in this" if percentage >= 60 else
            "🙂 Good Going! Keep up the good work!" if percentage >= 40 else
            "😕 You can do much better! Try again!"
    )
    
    cur = db.cursor()
    cur.execute(
        "INSERT INTO quiz_history (user_id, score, total, percentage) VALUES (%s,%s,%s,%s)",
        (session["user_id"], score, total, percentage)
    )
    db.commit()
    cur.close()

    return render_template("result.html", score=score, total=total, msg=msg)

# -------------------- HISTORY --------------------
@app.route("/history")
def history():
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT score,total,percentage,created_at FROM quiz_history WHERE user_id=%s ORDER BY created_at DESC",
        (session["user_id"],)
    )
    records = cur.fetchall()
    cur.close()
    return render_template("history.html", records=records)

@app.route("/delete-history", methods=["POST"])
def delete_history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    cur = db.cursor()
    cur.execute(
        "DELETE FROM quiz_history WHERE user_id = %s",
        (session["user_id"],)
    )
    db.commit()
    cur.close()

    flash("Quiz history deleted successfully.", "success")
    return redirect(url_for("history"))

@app.route("/delete-account", methods=["POST"])
def delete_account():
    if "user_id" not in session:
        return redirect(url_for("welcome"))

    password = request.form.get("password")
    user_id = session["user_id"]

    cur = db.cursor(dictionary=True)
    cur.execute("SELECT password_hash FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()

    if not user or not check_password_hash(user["password_hash"], password):
        flash("Incorrect password. Account not deleted.", "error")
        return redirect(url_for("index"))

    # delete history + user
    cur.execute("DELETE FROM quiz_history WHERE user_id = %s", (user_id,))
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    cur.close()

    session.clear()
    flash("Your account has been permanently deleted.", "success")
    return redirect(url_for("welcome"))

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form.get("username").strip()
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("forgot_password"))

        cur = db.cursor(dictionary=True)
        cur.execute("SELECT id FROM users WHERE TRIM(username)=%s", (username,))
        user = cur.fetchone()

        if not user:
            flash("User not found.", "error")
            cur.close()
            return redirect(url_for("forgot_password"))

        hashed = generate_password_hash(new_password)
        cur.execute(
            "UPDATE users SET password_hash=%s WHERE id=%s",
            (hashed, user["id"])
        )
        db.commit()
        cur.close()

        flash("Password updated successfully. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("forgot-password.html")

# -------------------- RUN --------------------
if __name__ == "__main__":
    app.run(debug=True)
