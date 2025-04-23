from flask import Blueprint, render_template, request, jsonify, redirect, url_for
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

@main_blueprint.route('/employees', methods=['GET', 'POST'])
def manage_employees():
    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            employee = Employee.objects.get(id=request.form.get('employee_id'))
            employee.name = request.form.get('name')
            employee.email = request.form.get('email')
            employee.cedula = request.form.get('cedula')
            employee.role = request.form.get('role')
            employee.save()
        else:
            employee = Employee(
                name=request.form.get('name'),
                email=request.form.get('email'),
                cedula=request.form.get('cedula'),
                role=request.form.get('role')
            )
            employee.save()
        return redirect(url_for('main.manage_employees'))

    employees = Employee.objects.all()
    return render_template('employees.html', employees=employees)

@main_blueprint.route('/employees/edit/<employee_id>', methods=['GET'])
def edit_employee(employee_id):
    employee = Employee.objects.get(id=employee_id)
    return render_template('edit_employee.html', employee=employee)

@main_blueprint.route('/employees/delete/<employee_id>')
def delete_employee(employee_id):
    Employee.objects.get(id=employee_id).delete()
    return redirect(url_for('main.manage_employees'))

@main_blueprint.route('/projects', methods=['GET', 'POST'])
def manage_projects():
    if request.method == 'POST':
        project = Project(
            name=request.form.get('name'),
            description=request.form.get('description'),
            end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d'),
            status='Active'
        )
        project.save()
        return redirect(url_for('main.manage_projects'))

    projects = Project.objects.all()
    return render_template('projects.html', projects=projects)

@main_blueprint.route('/projects/delete/<project_id>')
def delete_project(project_id):
    Project.objects.get(id=project_id).delete()
    return redirect(url_for('main.manage_projects'))

@main_blueprint.route('/tasks', methods=['GET', 'POST'])
def get_tasks():
    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            task = Task.objects.get(id=request.form.get('task_id'))
            task.description = request.form.get('description')
            task.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
            task.estimated_days = int(request.form.get('estimated_days'))
            task.status = request.form.get('status')
            task.employee_id = Employee.objects.get(id=request.form.get('employee_id'))
            task.project_id = Project.objects.get(id=request.form.get('project_id'))
            task.save()
        else:
            task = Task(
                description=request.form.get('description'),
                start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d'),
                estimated_days=int(request.form.get('estimated_days')),
                status=request.form.get('status'),
                employee_id=Employee.objects.get(id=request.form.get('employee_id')),
                project_id=Project.objects.get(id=request.form.get('project_id'))
            )
            task.save()
        return redirect(url_for('main.get_tasks'))

    tasks = Task.objects.all()
    tasks_by_status = {
        'Not Started': [],
        'In Progress': [],
        'Completed': []
    }
    
    current_date = datetime.now()
    for task in tasks:
        task.days_elapsed = (current_date.date() - task.start_date).days
        if task.status == 'Completed':
            task.completion_days = task.days_elapsed
        tasks_by_status[task.status].append(task)

    employees = Employee.objects.all()
    projects = Project.objects.all()
    return render_template('tasks.html', 
                         tasks_by_status=tasks_by_status,
                         employees=employees, 
                         projects=projects)

@main_blueprint.route('/tasks/edit/<task_id>', methods=['GET'])
def edit_task(task_id):
    task = Task.objects.get(id=task_id)
    employees = Employee.objects.all()
    projects = Project.objects.all()
    return render_template('edit_task.html', task=task, employees=employees, projects=projects)

@main_blueprint.route('/overdue-tasks')
def overdue_tasks():
    current_date = datetime.now().date()
    all_tasks = Task.objects.all()
    
    task_status = {
        'overdue': [],
        'in_progress': [],
        'completed': []
    }

    for task in all_tasks:
        task_due_date = task.start_date + timedelta(days=task.estimated_days)
        task.due_date = task_due_date
        task.days_elapsed = (current_date - task.start_date).days
        
        if task.status == 'Completed':
            task.completion_days = task.days_elapsed
            task_status['completed'].append(task)
        elif task.status == 'In Progress':
            if task_due_date < current_date:
                task.days_past_due = (current_date - task_due_date).days
                task.overdue = True
                task_status['overdue'].append(task)
            else:
                task_status['in_progress'].append(task)

    return render_template('overdue_tasks.html', task_status=task_status)
