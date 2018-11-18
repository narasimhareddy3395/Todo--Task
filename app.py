from flask import Flask, render_template, request, jsonify, url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////sqlite3/todo.db'

db = SQLAlchemy(app)

z = ""


# This Class Creates table for TaskList
class TaskList(db.Model):
    __tablename__ = 'TaskList'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column("name", db.String(200))
    tasks = db.Column("tasks", db.String(300))


# This Class Creates table for Task
class Task(db.Model):
    __tablename__ = 'Task'
    SNo = db.Column("Sno", db.Integer, primary_key=True, autoincrement=True)
    id = db.Column('id', db.Integer, db.ForeignKey("TaskList.id"))
    name = db.Column("name", db.Unicode)
    tasks = db.Column("tasks", db.Boolean)


# Home Page
@app.route('/api')
def index():
    return render_template('index.html')


# This function returns the template for New User.
@app.route('/api/tasks')
def api():
    return render_template('tasklist.html')


# This function adds  TaskLists into the Table TaskList.
@app.route('/add', methods=['POST'])
def add():
    sodo = TaskList(id=request.form['id'], name=request.form['name'], tasks=request.form['tasks'])
    db.session.add(sodo)
    db.session.commit()
    todo = TaskList.query.filter_by(id=int(request.form['id'])).first()
    id = todo.id
    print(id)
    result = (todo.tasks)
    res = result.split(",")
    print(res)
    for name in res:
        todo = Task(id=id, name=name, tasks=False)
        db.session.add(todo)
        db.session.commit()
    print(id)
    return redirect(url_for("complete", id=int(request.form['id'])))


# This function adds the new task for existing Task List
@app.route("/newtask", methods=["POST"])
def newtask():
    print("HI")
    todo = Task(id=z, name=(request.form['tsk']), tasks=False)
    db.session.add(todo)
    db.session.commit()
    print(z)
    print(todo)
    return redirect(url_for("complete", id=z))


# This function returns the Todo Lists of User.
@app.route('/api/task/<id>')
def complete(id):
    global z
    incomplete = Task.query.filter_by(id=int(id), tasks=False).all()
    complete = Task.query.filter_by(id=int(id), tasks=True).all()
    nm = TaskList.query.filter_by(id=int(id)).all()
    z = int(id)
    return render_template('display.html', incomplete=incomplete, complete=complete, name=nm)


# This function updates the Task completion
@app.route('/complete/<id>')
def completed(id):
    todo = Task.query.filter_by(id=int(id), tasks=False).first()
    todo.tasks = True
    db.session.commit()
    print(todo)
    return redirect(url_for('complete', id=id))

if __name__ == '__main__':
    app.run(debug=True)
