# MiniCore

MiniCore is a Flask-based web application for managing employees, tasks, and projects. It allows users to view overdue tasks within a specified date range, filter tasks based on status and date, and track the progress of various projects.

## Features

- View all employees, tasks, and projects.
- Filter overdue tasks within a specified date range.
- Highlight the total number of overdue tasks.
- Simple, user-friendly interface.

## Prerequisites

- Python 3.11
- SQLite
- Flask
- SQLAlchemy
- Jinja2

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/minicore.git
    cd minicore
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. Populate the database with initial data:

    ```bash
    sqlite3 instance/minicore.sqlite < data.sql
    ```

## Usage

1. Run the Flask application:

    ```bash
    flask run
    ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

## File Structure


## Models

### Employee

- `id`: Integer, primary key
- `first_name`: String, employee's first name
- `last_name`: String, employee's last name
- `username`: String, unique, employee's username
- `tasks`: Relationship to `Task`

### Project

- `id`: Integer, primary key
- `name`: String, project's name
- `tasks`: Relationship to `Task`

### Task

- `id`: Integer, primary key
- `description`: String, task description
- `start_date`: DateTime, task start date
- `estimated_days`: Integer, estimated number of days to complete the task
- `status`: String, task status (e.g., 'In progress', 'Done')
- `employee_id`: Integer, foreign key to `Employee`
- `project_id`: Integer, foreign key to `Project`
- `employee`: Relationship to `Employee`
- `project`: Relationship to `Project`

## Routes

### `/`

Displays the homepage with a list of employees, tasks, and projects.

### `/overdue-tasks`

Displays a list of overdue tasks within a specified date range. Users can filter tasks by start and end dates.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Bootstrap](https://getbootstrap.com/)
