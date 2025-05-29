# Training Management System

A MySQL-based training management system for tracking students, organizations, supervisors, and training reports.

## Features

- Student management with academic information
- Organization tracking
- Internal and external supervisor management
- Training report submission and evaluation
- User role management (admin, trainer, trainee, supervisor)

## Requirements

- Python 3.x
- MySQL Server
- `mysql-connector-python` package

## Setup

1. Install the required package:
```bash
pip install mysql-connector-python
```

2. Configure your MySQL connection:
   - Update the database credentials in `db_connection.py`
   - Default credentials:
     - Host: localhost
     - User: root
     - Password: mahmoud
     - Database: training_mm

3. Initialize the database:
```bash
python db_connection.py
```

## Database Schema

The system includes the following tables:
- students
- organizations
- internal_supervisors
- external_supervisors
- training_reports
- evaluations
- users

## Security Note

Please change the default database credentials before deploying to production. 