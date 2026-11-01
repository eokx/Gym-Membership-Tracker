Gym Membership & Attendance Tracker
A beginner-friendly gym management web application built with Python
Flask and MySQL. The project provides a dashboard for viewing gym
information and separate pages for managing members, membership plans,
attendance records, and trainers.
Project Description
The Gym Membership & Attendance Tracker is designed to help a gym
administrator keep basic gym records organized in one place. It connects
a Flask web application to a MySQL database and displays database
records through HTML templates.
The project is suitable as an academic mini-project demonstrating Python
web development, SQL database connectivity, CRUD-style operations, and
server-side page rendering.
Technologies Used
Python 3.13
Flask -- web framework
MySQL -- relational database
MySQL Connector/Python -- database connectivity
HTML and CSS -- user interface
Jinja2 -- dynamic HTML templates (included with Flask)
Visual Studio Code -- development environment
Features
Dashboard showing total members, membership plans, attendance
records, and revenue.
Members page displaying member details.
Add Member form to save a new member in MySQL.
Edit Member form to update an existing member.
Membership Plans page displaying available plans.
Attendance page displaying attendance records with member names.
Attendance Check-in form to record a member's entry time.
Check-out route to record a member's exit time.
Trainers page displaying trainer information.
> **Project status:** The main pages and routes have been added. Test
> the Add Member, Edit Member, Check-in, and Check-out workflows with
> your own database before presenting the project. The Delete Member
> feature is currently not part of the active workflow.
Project Structure
``` text
Gym_Membership_Tracker/
│
├── app.py
│
└── templates/
    ├── index.html
    ├── members.html
    ├── add_member.html
    ├── edit_member.html
    ├── plans.html
    ├── attendance.html
    ├── checkin.html
    └── trainers.html
```
Your project may also contain the exported database file:
``` text
gym_membership_tracker.sql
```
Keep the SQL export in a safe location. Do not commit database passwords
or private information to GitHub.
Database
Database name: `gym_membership_tracker`
The application uses these tables:
`members`
`membership_plans`
`memberships`
`attendance`
`trainers`
The Flask routes expect the columns referenced in the SQL queries in
`app.py`. If your database uses different column names, update the
queries to match your actual schema.
Setup and Installation
1. Install Python and MySQL
Install Python 3.13 and MySQL Server. Make sure your MySQL service is
running.
2. Clone the repository
``` bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd Gym_Membership_Tracker
```
Replace the example GitHub URL with your repository URL.
3. Create and activate a virtual environment (recommended)
On Windows:
``` bash
python -m venv venv
venv\Scripts\activate
```
4. Install dependencies
``` bash
python -m pip install flask mysql-connector-python
```
5. Create the MySQL database
Open MySQL Workbench and create or import the database named:
``` sql
CREATE DATABASE gym_membership_tracker;
```
If you have the project SQL export, import `gym_membership_tracker.sql`
into MySQL Workbench. Confirm that all five tables exist before starting
the application.
6. Configure the database connection
Open `app.py` and configure `get_db_connection()` with your local MySQL
settings:
``` python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="gym_membership_tracker"
    )
```
Replace `YOUR_MYSQL_PASSWORD` with your own local MySQL password.
Never publish your real password on GitHub. For a public repository,
move credentials into environment variables before uploading.
7. Run the application
From the project folder, run:
``` bash
python app.py
```
Open this address in your browser:
``` text
http://127.0.0.1:5000
```
Keep the terminal running while using the application. Press `Ctrl + C`
in the terminal to stop the Flask server.
Main Routes
Page / Operation       Route
---
Dashboard              `/`
Members                `/members`
Add Member             `/add-member`
Edit Member            `/edit-member/<member_id>`
Membership Plans       `/plans`
Attendance             `/attendance`
Attendance Check-in    `/checkin`
Attendance Check-out   `/checkout/<attendance_id>`
Trainers               `/trainers`
Future Improvements
Add membership assignment and renewal workflows.
Add member search and filtering.
Add validation and clearer success/error messages.
Improve responsive design and navigation.
Add role-based administrator login.
Move database credentials to environment variables.
Add automated tests and stronger error handling.
Add reports for attendance and membership revenue.
Learning Outcomes
This project demonstrates:
Connecting a Python Flask application to MySQL.
Writing SQL `SELECT`, `INSERT`, and `UPDATE` queries.
Displaying database records using Flask and Jinja2 templates.
Handling HTML form submissions using HTTP GET and POST.
Organizing a small web application into routes and templates.
Author
Samar Sharma
MCA -- Data Science  
License
This project is intended for educational and academic use. Add a license
if you plan to distribute or reuse it publicly.
