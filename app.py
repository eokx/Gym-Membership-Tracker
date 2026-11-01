
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="system",
        database="gym_membership_tracker"
    )


# Dashboard page
@app.route("/")
def dashboard():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Total members
    cursor.execute("SELECT COUNT(*) AS total FROM members")
    total_members = cursor.fetchone()["total"]

    # Total membership plans
    cursor.execute("SELECT COUNT(*) AS total FROM membership_plans")
    total_plans = cursor.fetchone()["total"]

    # Total attendance records
    cursor.execute("SELECT COUNT(*) AS total FROM attendance")
    total_attendance = cursor.fetchone()["total"]

    # Total revenue
    cursor.execute("SELECT COALESCE(SUM(paid_amount), 0) AS revenue FROM memberships")
    total_revenue = cursor.fetchone()["revenue"]

    # Recent members
    cursor.execute("""
        SELECT member_id, full_name, age, phone
        FROM members
        ORDER BY member_id DESC
        LIMIT 5
    """)
    recent_members = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "index.html",
        total_members=total_members,
        total_plans=total_plans,
        total_attendance=total_attendance,
        total_revenue=total_revenue,
        recent_members=recent_members
    )

# Members page

# Membership Plans page
@app.route("/plans")
def plans():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT plan_id, plan_name, duration_months,
               price, description
        FROM membership_plans
        ORDER BY plan_id
    """)

    all_plans = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "plans.html",
        plans=all_plans
    )


@app.route("/members")
def members():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT member_id, full_name, age, gender,
               phone, email, join_date
        FROM members
        ORDER BY member_id DESC
    """)

    all_members = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "members.html",
        members=all_members
    )

# Attendance page
@app.route("/attendance")
def attendance():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            a.attendance_id,
            m.full_name,
            a.attendance_date,
            a.check_in,
            a.check_out
        FROM attendance a
        INNER JOIN members m
            ON a.member_id = m.member_id
        ORDER BY a.attendance_date DESC, a.check_in DESC
    """)

    attendance_records = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "attendance.html",
        attendance_records=attendance_records
    )

# Trainers page
@app.route("/trainers")
def trainers():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            trainer_id,
            trainer_name,
            specialization,
            phone,
            email,
            salary,
            hire_date
        FROM trainers
        ORDER BY trainer_id
    """)

    all_trainers = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "trainers.html",
        trainers=all_trainers
    )
# Add New Member
@app.route("/add-member", methods=["GET", "POST"])
def add_member():

    if request.method == "POST":

        full_name = request.form["full_name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        email = request.form.get("email") or None

        db = get_db_connection()
        cursor = db.cursor()

        sql = """
            INSERT INTO members
            (full_name, age, gender, phone, email, join_date)
            VALUES (%s, %s, %s, %s, %s, CURDATE())
        """

        values = (full_name, age, gender, phone, email)

        cursor.execute(sql, values)
        db.commit()

        cursor.close()
        db.close()

        return redirect(url_for("members"))

    return render_template("add_member.html")

# Delete Member
@app.route("/delete-member/<int:member_id>", methods=["POST"])
def delete_member(member_id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM members WHERE member_id = %s",
        (member_id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("members"))


# Edit Member
@app.route("/edit-member/<int:member_id>", methods=["GET", "POST"])
def edit_member(member_id):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        full_name = request.form["full_name"]
        age = request.form["age"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        email = request.form.get("email") or None

        cursor.execute("""
            UPDATE members
            SET full_name = %s,
                age = %s,
                gender = %s,
                phone = %s,
                email = %s
            WHERE member_id = %s
        """, (full_name, age, gender, phone, email, member_id))

        db.commit()

        cursor.close()
        db.close()

        return redirect(url_for("members"))

    cursor.execute(
        "SELECT * FROM members WHERE member_id = %s",
        (member_id,)
    )

    member = cursor.fetchone()

    cursor.close()
    db.close()

    if member is None:
        return "Member not found", 404

    return render_template("edit_member.html", member=member)


# Attendance Check-in
@app.route("/checkin", methods=["GET", "POST"])
def checkin():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":

        member_id = request.form["member_id"]

        cursor.execute("""
            INSERT INTO attendance
            (member_id, attendance_date, check_in)
            VALUES (%s, CURDATE(), CURTIME())
        """, (member_id,))

        db.commit()

        cursor.close()
        db.close()

        return redirect(url_for("attendance"))

    cursor.execute("""
        SELECT member_id, full_name
        FROM members
        ORDER BY full_name
    """)

    all_members = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "checkin.html",
        members=all_members
    )

# Attendance Check-out
@app.route("/checkout/<int:attendance_id>", methods=["POST"])
def checkout(attendance_id):

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE attendance
        SET check_out = CURTIME()
        WHERE attendance_id = %s
        AND check_out IS NULL
    """, (attendance_id,))

    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("attendance"))


if __name__ == "__main__":
    app.run(debug=True)
