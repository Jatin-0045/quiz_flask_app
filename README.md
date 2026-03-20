# IntelliQuiz – Full Stack Quiz Web Application

A full-stack quiz web application built using Flask and MySQL, featuring secure user authentication, real-time quiz generation via API integration, and persistent performance tracking. Designed with production-ready practices including environment-based configuration and deployment on cloud platforms.

🌐 **Live Demo**  
Currently not hosted (Railway trial expired). The application can be run locally by following the steps in the **Local Installation & Setup** section below.

---

## 🔥 Features

* User signup, login, logout
* Secure password hashing using Werkzeug
* Dynamic quiz questions (Open Trivia API)
* Score calculation with result feedback
* Quiz history tracking for logged-in users
* Forgot password & delete account functionality
* Session management
* Responsive UI with Bootstrap

---

## 🚀 Key Highlights

- Implemented environment-based database configuration for both local and cloud deployments.
- Handled real-world deployment challenges including MySQL connectivity and service configuration.
- Designed modular Flask architecture with clear separation of routes, templates, and static assets.

---

## 🧠 Tech Stack

| Technology | Description                |
| ---------- | -------------------------- |
| Python     | Backend logic              |
| Flask      | Web framework              |
| MySQL      | Database (Railway + Local) |
| HTML / CSS | Frontend                   |
| Bootstrap  | Responsive UI              |
| JavaScript | Quiz logic & API calls     |
| Gunicorn   | Production WSGI server     |
| Railway    | Deployment platform        |

---

## 📁 Project Structure

```
quiz_flask_app/
│
├── app.py
├── requirements.txt
├── Procfile
├── .env.example
├── db/
│   └── schema.sql
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── favicon/
│       └── intelliquiz-favicon.svg
├── templates/
│   ├── welcome.html
│   ├── signup.html
│   ├── login.html
│   ├── index.html
│   ├── quiz.html
│   ├── result.html
│   ├── history.html
│   └── forgot-password.html
└── screenshots/
```

---


---

## 🚀 Local Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/quiz_flask_app.git
cd quiz_flask_app
```

### 2️⃣ Create & activate virtual environment (Windows)
python 
-m venv venv
venv\Scripts\activate

### 3️⃣ Install dependencies
pip install -r requirements.txt

### 4️⃣ Configure environment variables

Create a .env file:
MYSQLHOST=localhost
MYSQLUSER=root
MYSQLPASSWORD=your_password
MYSQLDATABASE=intelliquiz
MYSQLPORT=3306
SECRET_KEY=intelliquiz_secret_key

### 5️⃣ Setup database

Run the schema file located at:
db/schema.sql

### 6️⃣ Run the app
python app.py

### Open in browser:
http://localhost:5000

## 🖼️ Screenshots

🖼️ Screenshots

Homepage:  
![Homepage](static/screenshots/homepage.png)

Login page:  
![Login](static/screenshots/login.png)

Signup page:  
![Signup](static/screenshots/signup.png)

Quiz page:  
![Quiz](static/screenshots/quiz.png)

History page:  
![History](static/screenshots/history.png)

Result page:  
![Result](static/screenshots/result.png)

---

## 🌐 Deployment (Railway)

This project was deployed on **Railway** using **Gunicorn**.

**Key Deployment Notes:**

* Uses Railway MySQL service
* Environment variables configured via Railway dashboard

* `Procfile`:
```
web: gunicorn app:app
```
## 👤 Author

**Jatin Morwal**

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub — it really helps!
