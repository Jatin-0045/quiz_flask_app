from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="intelliquiz"
    )

def create_user(username, password):
    db = get_db()
    cursor = db.cursor()
    hashed = generate_password_hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed)
        )
        db.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        db.close()

def authenticate_user(username, password):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE username = %s",
        (username,)
    )
    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user and check_password_hash(user["password_hash"], password):
        return user
    return None
