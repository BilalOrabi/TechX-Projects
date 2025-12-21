# Student Success Tracker

A production-ready CLI tool for managing student records with SQLite. Track student information, GPA, academic status, and more.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python3 success_tracker.py init-db
   ```

## Usage

**Initialize database with demo students:**
```bash
python3 success_tracker.py init-db --seed
```

**Add a new student:**
```bash
python3 success_tracker.py add --name "Mohammad abdo" --email moh@example.com --major "Computer Science" --gpa 3.8 --status active
```

**List all students (sorted by GPA):**
```bash
python3 success_tracker.py list
```

**Filter students by status:**
```bash
python3 success_tracker.py list --status probation
```

**Find students by major:**
```bash
python3 success_tracker.py find-major "Mathematics"
```

**Update a student's GPA:**
```bash
python3 success_tracker.py update-gpa --id 1 --gpa 3.9
```

**Delete a student:**
```bash
python3 success_tracker.py delete --id 1
```
