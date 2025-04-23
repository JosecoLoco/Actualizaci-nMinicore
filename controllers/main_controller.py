from flask import Blueprint, render_template, request, jsonify
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
    employees = Employee.objects.all()
    tasks = Task.objects.all()
    projects = Project.objects.all()
    return render_template('base.html', employees=employees, tasks=tasks, projects=projects)

@main_blueprint.route('/employees')
def get_employees():
    employees = Employee.objects.all()
    return jsonify([emp.serialize() for emp in employees])

@main_blueprint.route('/projects')
def get_projects():
    projects = Project.objects.all()
    return jsonify([proj.serialize() for proj in projects])

@main_blueprint.route('/tasks')
def get_tasks():
    tasks = Task.objects.all()
    return jsonify([task.serialize() for task in tasks])

@main_blueprint.route('/overdue-tasks')
def overdue_tasks():
    start_date_str = request.args.get('start_date', '2024-01-06')
    end_date_str = request.args.get('end_date', '2024-12-31')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    tasks_in_progress = Task.objects(
        status='In progress',
        start_date__gte=start_date,
        start_date__lte=end_date
    )

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
