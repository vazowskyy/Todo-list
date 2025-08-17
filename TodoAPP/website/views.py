from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Task
from . import db
views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/todo_list', methods=['GET', 'POST'])
@login_required
def todo_list():
    if request.method == 'POST':
        name = request.form.get('name')
        text = request.form.get('content')

        task = Task(name=name, text=text, user=current_user.id)
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('views.todo_list'))

    return render_template("todo_list.html")


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
