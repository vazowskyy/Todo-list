from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from .models import Task
from . import db
from .forms import TaskAddForm, TaskEditForm, TaskCategorySearch
views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/todo_list', methods=['GET', 'POST'])
@login_required
def todo_list():
    form = TaskAddForm()
    search = TaskCategorySearch()
    if search.submit.data and request.method == 'POST':
        filter = f"%{search.category.data}%"
        tasks = Task.query.filter(Task.category.like(filter),
                                  Task.user == current_user.id).all()
        return render_template("todo_list.html", form=form, search=search, tasks=tasks)
    if request.method == 'POST':
        name = form.name.data
        text = form.content.data
        category = form.category.data
        task = Task(name=name, text=text,
                    category=category, user=current_user.id)
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('views.todo_list'))

    return render_template("todo_list.html", form=form, search=search, tasks=current_user.tasks)


@views.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    if request.method == 'POST':
        task = Task.query.filter_by(
            id=task_id, user=current_user.id).first()
        if task:
            db.session.delete(task)
            db.session.commit()
    return redirect(url_for('views.todo_list'))


@views.route('/task_completed/<int:task_id>', methods=['POST'])
@login_required
def task_completed(task_id):
    if request.method == 'POST':
        task = Task.query.filter_by(id=task_id, user=current_user.id).first()
        if task:
            task.completed = not task.completed
            db.session.commit()

    return redirect(url_for('views.todo_list'))


@views.route('/task_edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task_edit(task_id):
    form = TaskEditForm()
    task = Task.query.filter_by(id=task_id, user=current_user.id).first()
    if task:
        if request.method == 'POST':
            task.name = form.name.data
            task.text = form.content.data
            task.date = func.now()
            task.category = form.category.data
            task.completed = True if form.completed.data else False
            db.session.commit()
            return redirect(url_for('views.todo_list'))
        return render_template('task_edit.html', task=task, form=form)
    return redirect(url_for('views.todo_list'))
