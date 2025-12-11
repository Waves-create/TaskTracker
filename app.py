from flask import Flask,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TaskTracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class TaskTracker(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    due_date = db.Column(db.Date)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
with app.app_context():
    db.create_all()
    
@app.route("/",methods=['GET','POST'])
def home():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        due_date_str=request.form['due_date']
        due_date=datetime.strptime(due_date_str, '%Y-%m-%d').date()
        task_tracker=TaskTracker(title=title,desc=desc,due_date=due_date)
        db.session.add(task_tracker)
        db.session.commit()
    all_tasks=TaskTracker.query.all()
    return render_template("index.html", all_tasks=all_tasks)

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        due_date_str=request.form['due_date']
        due_date=datetime.strptime(due_date_str, '%Y-%m-%d').date()
        task=TaskTracker.query.filter_by(sno=sno).first()
        task.title=title
        task.desc=desc
        task.due_date=due_date
        db.session.add(task)
        db.session.commit()
        return redirect("/")
    task=TaskTracker.query.filter_by(sno=sno).first()
    return render_template("update.html",task=task)

@app.route("/delete/<int:sno>")
def delete(sno):
    task=TaskTracker.query.filter_by(sno=sno).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)