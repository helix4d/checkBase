# CheckBase

Django 5.0 project for managing course evaluations with faculty, departments, instructors, courses, course elements, and scores on a five-point scale. All tables are available through the Django admin with CRUD support.

## Getting started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Apply database migrations (SQLite by default):
   ```bash
   python manage.py migrate
   ```
3. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Access credentials and security

- The entire site is protected with HTTP Basic Authentication. Use:
  - **Username:** `admin`
  - **Password:** `Admin#184!`
- A Django superuser with the same credentials is created by migrations for accessing the admin site at `/admin/`.

## Data model highlights

- **Faculty** and **Department** tables organize instructors and courses.
- **Instructor** links to both faculty and department.
- **Course** belongs to a department and faculty.
- **CourseElement** covers contact data, course description, lectures, assignments, and global group synchronization blocks.
- **Score** stores five-point ratings per course element and instructor.
- **InstructorStats** maintains rating counts and averages per instructor.
