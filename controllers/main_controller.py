from flask import Blueprint, render_template, request
from models import Employee, Task, Project
from utils.database import db
from datetime import datetime, timedelta

main_blueprint = Blueprint('main', __name__)

def calculate_business_days(start_date, end_date):
    day_generator = (start_date + timedelta(x) for x in range((end_date - start_date).days + 1))
    business_days = sum(1 for day in day_generator if day.weekday() < 5)
    return business_days

@main_blueprint.route('/')
def index():
    employees = Employee.query.all()
    tasks = Task.query.all()
    projects = Project.query.all()
    return render_template('base.html', employees=employees, tasks=tasks, projects=projects)

@main_blueprint.route('/overdue-tasks')
def overdue_tasks():
    start_date_str = request.args.get('start_date', '2024-01-06')
    end_date_str = request.args.get('end_date', '2024-01-14')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Obtén las tareas en progreso dentro del rango de fechas
    tasks_in_progress = Task.query.filter(
        Task.status == 'In progress',
        Task.start_date >= start_date,
        Task.start_date <= end_date
    ).all()

    overdue_tasks = []
    for task in tasks_in_progress:
        task_due_date = task.start_date + timedelta(days=task.estimated_days)
        task.due_date = task_due_date
        if task_due_date < end_date:
            business_days_diff = calculate_business_days(task_due_date, end_date)
            task.days_past_due = business_days_diff
            task.overdue = True
            overdue_tasks.append(task)

    return render_template('overdue_tasks.html', tasks=overdue_tasks)
