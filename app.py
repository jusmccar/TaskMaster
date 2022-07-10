from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import path

DB_NAME = "database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_NAME
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id

@app.before_first_request
def create_database():
    if not path.exists(DB_NAME):
        db.create_all()

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Task(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for(".index"))
        except:
            return "There was an issue adding that task."
    else:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template("index.html", tasks=tasks)

@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form["content"]

        try:
            db.session.commit()
            return redirect(url_for(".index"))
        except:
            return "There was an issue updating that task."
    else:
        return render_template("update.html", task=task)

@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for(".index"))
    except:
        return "There was an issue deleting that task."

if __name__ == "__main__":
    app.run(debug=True)
