import sqlite3
from datetime import datetime, timezone

connection_string = "success_tracker.db"


# =========================
# SQL STATEMENTS 
# =========================

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    major TEXT NOT NULL,
    gpa REAL CHECK (gpa BETWEEN 0 AND 4),
    status TEXT CHECK (status IN ('active','probation','graduated')) DEFAULT 'active',
    last_updated TEXT NOT NULL
);
"""

CREATE_INDEX_MAJOR_SQL = """
CREATE INDEX IF NOT EXISTS idx_students_major
ON students (major);
"""


INSERT_STUDENT_SQL = """
INSERT INTO students (name, email, major, gpa, status, last_updated)
VALUES (?, ?, ?, ?, ?, ?);
"""

SELECT_ALL_SQL = """
SELECT * FROM students
ORDER BY gpa DESC;
"""

SELECT_BY_STATUS_SQL = """
SELECT * FROM students
WHERE status = ?
ORDER BY gpa DESC;
"""

SELECT_BY_MAJOR_SQL = """
SELECT * FROM students
WHERE major = ?;
"""

SELECT_BY_ID_SQL = """
SELECT * FROM students
WHERE id = ?;
"""

UPDATE_GPA_SQL = """
UPDATE students
SET gpa = ?, last_updated = ?
WHERE id = ?;
"""

DELETE_STUDENT_SQL = """
DELETE FROM students
WHERE id = ?;
"""


# =========================
# HELPERS
# =========================

def _utc_now():
    return datetime.now(timezone.utc).isoformat()


# =========================
# PUBLIC METHODS
# =========================

def create_students_table():
    with sqlite3.connect(connection_string) as connection:
        try:
            connection.execute(CREATE_TABLE_SQL)
            connection.execute(CREATE_INDEX_MAJOR_SQL)
        except sqlite3.Error as e:
            raise ValueError(f"Failed to create students table: {e}") from e


def add_student(name, email, major, gpa, status="active"):
    if not (0 <= gpa <= 4):
        raise ValueError("GPA must be between 0 and 4")

    allowed_statuses = ("active", "probation", "graduated")
    if status not in allowed_statuses:
        raise ValueError(f"Status must be one of {allowed_statuses}")

    timestamp = _utc_now()

    try:
        with sqlite3.connect(connection_string) as connection:
            cursor = connection.cursor()
            cursor.execute(INSERT_STUDENT_SQL, (name, email, major, gpa, status, timestamp))
            return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        if "students.email" in str(e):
            raise ValueError("Email already exists") from e
        

    except sqlite3.Error as e:
        raise ValueError(f"Failed to add student: {e}") from e


def seed_demo_students(demo_students=None):
    
    default = [
        ("Bilal", "bilal@example.com", "Physics", 3.5, "active"),
        ("ahmad", "ahmad@example.com", "Computer Science", 2.8, "probation"),
    ]
    students = demo_students or default
    inserted = 0
    for name, email, major, gpa, status in students:
        try:
            add_student(name, email, major, gpa, status)
            inserted += 1
        except ValueError as e:
            if "Email already exists" in str(e):
                continue
            raise
    return inserted


def get_students(status=None):
    with sqlite3.connect(connection_string) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        try:
            if status:
                cursor.execute(SELECT_BY_STATUS_SQL, (status,))
            else:
                cursor.execute(SELECT_ALL_SQL)
        except sqlite3.Error as e:
            raise ValueError(f"Failed to retrieve students: {e}") from e

        return cursor.fetchall()


def find_by_major(major):
    with sqlite3.connect(connection_string) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            cursor.execute(SELECT_BY_MAJOR_SQL, (major,))
        except sqlite3.Error as e:
            raise ValueError(f"Failed to find students by major '{major}': {e}") from e
        return cursor.fetchall()


def get_student_by_id(student_id):
    with sqlite3.connect(connection_string) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        try:
            cursor.execute(SELECT_BY_ID_SQL, (student_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            raise ValueError(f"Failed to fetch student {student_id}: {e}") from e


def update_student(student_id, name=None, email=None, major=None, gpa=None, status=None):
    
    name = None if name == "" else name
    email = None if email == "" else email
    major = None if major == "" else major
    status = None if status == "" else status
    
    if gpa is not None:
        if not (0 <= gpa <= 4):
            raise ValueError("GPA must be between 0 and 4")
    
    if status is not None:
        allowed_statuses = ("active", "probation", "graduated")
        if status not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
    
    params = []
    set_clauses = []
    
    if name is not None:
        set_clauses.append("name = ?")
        params.append(name)
    
    if email is not None:
        set_clauses.append("email = ?")
        params.append(email)
    
    if major is not None:
        set_clauses.append("major = ?")
        params.append(major)
    
    if gpa is not None:
        set_clauses.append("gpa = ?")
        params.append(gpa)
    
    if status is not None:
        set_clauses.append("status = ?")
        params.append(status)
    
    if not set_clauses:
        raise ValueError("No fields provided to update")
    
    set_clauses.append("last_updated = ?")
    params.append(_utc_now())
    params.append(student_id)
    
    sql = f"UPDATE students SET {', '.join(set_clauses)} WHERE id = ?;"
    
    try:
        with sqlite3.connect(connection_string) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, tuple(params))
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        raise ValueError(f"Failed to update student {student_id}: {e}") from e


def update_gpa(student_id, gpa):
    if not (0 <= gpa <= 4):
        raise ValueError("GPA must be between 0 and 4")

    timestamp = _utc_now()

    with sqlite3.connect(connection_string) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(UPDATE_GPA_SQL, (gpa, timestamp, student_id))
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            raise ValueError(f"Failed to update GPA for student {student_id}: {e}") from e


def delete_student(student_id):
    with sqlite3.connect(connection_string) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(DELETE_STUDENT_SQL, (student_id,))
        except sqlite3.Error as e:
            raise ValueError(f"Failed to delete student {student_id}: {e}") from e
        return cursor.rowcount
