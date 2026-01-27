Quiz Flask App
A simple and interactive quiz application built using Flask. Users can sign up, log in, take quizzes, view results, and track their quiz history.

🔥 Features
•	User Signup and Login
•	Secure Password Hashing
•	Quiz Questions with Scoring
•	Result Page with Score Summary
•	Quiz History for Logged-in Users
•	Responsive UI using Bootstrap

🧠 Tech Stack
Technology	Description
Python	Backend logic
Flask	Web framework
SQLite	Database
HTML/CSS	Frontend
Bootstrap	Responsive UI
JavaScript	Quiz logic

📁 Project Structure
quiz_flask_app/
│
├── app.py
├── requirements.txt
├── db/
│   └── schema.sql
├── instance/
│   └── (database file)
├── utils/
│   └── auth.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── favicon/
│       └── intelliquiz-favicon.svg
└── templates/
    ├── index.html
    ├── login.html
    ├── signup.html
    ├── quiz.html
    ├── result.html
    ├── history.html
    ├── forgot-password.html
    └── welcome.html

🚀 Installation
1.	1. Clone the repository
git clone https://github.com/yourusername/quiz_flask_app.git
cd quiz_flask_app
2.	2. Create a virtual environment
python -m venv venv
3.	3. Activate the virtual environment (Windows)
venv\Scripts\activate
4.	4. Install dependencies
pip install -r requirements.txt
5.	5. Run the app
python app.py
Open your browser:
http://localhost:5000

📌 Database Setup
The database schema is located in:
db/schema.sql
Run the SQL script to create the required tables.

🖼️ Screenshots
Add screenshots to the screenshots/ folder and update the file names accordingly.
Homepage / Login page
Quiz page
Result page

🌐 Deployment
You can deploy this app on platforms like:
•	Render
•	Heroku
•	PythonAnywhere
Live demo link will be added here after deployment:
Live Demo: https://your-app-link.com

👤 Author
Jatin Morwal

⭐ Support
If you liked this project, give it a ⭐ on GitHub!
