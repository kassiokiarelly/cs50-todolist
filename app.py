from flask import Flask, request, render_template, redirect
from db import get_tasks_all, get_task_by_id, get_tasks_by_status, insert_task, update_task, task_done

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
def index():
    return redirect("/Tasks/Pending")

@app.route('/Tasks/<name>')
def tasks(name : ''):
    name = str(name).lower()
    if name == 'pending':
        tasks = get_tasks_by_status('Pending')
        return render_template("tasks/pending.html", tasks = tasks)
    if name == 'done':
        tasks = get_tasks_by_status('Done')        
        return render_template("tasks/done.html", tasks = tasks)
    if name == 'all':
        tasks = get_tasks_all()
        return render_template("tasks/all.html", tasks = tasks)
    if name == 'add':
        return render_template("tasks/add.html")
    else:
        return redirect("/Tasks/Pending")


@app.route('/Tasks/Add', methods = ['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    insert_task(title, description)
    return redirect('/Tasks/ToDo')

@app.route('/Tasks/<int:id>', methods = ['GET'])
def get_task(id):
    task = get_task_by_id(id)
    if len(task) > 0:
        return render_template("tasks/detail.html", tasks = task)


@app.route('/Tasks/<int:id>/Edit', methods = ['GET', 'POST'])
def edit_task(id):
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        update_task(id, title, description)
        return redirect(f"/Tasks/{id}")
    else:
        task = get_task_by_id(id)
        if len(task) > 0:
            return render_template("tasks/edit.html", task = task[0])
        return redirect("/Tasks/ToDo")


@app.route('/Tasks/<int:id>/Done', methods = ['GET'])
def mark_task_done(id):
    task_done(id)
    return redirect(f"/Tasks/{id}")       