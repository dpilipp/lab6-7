from flask import Flask
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    group = db.Column(db.String(10), nullable = False)
    marks = db.Column(db.Text, default = '')

    def __repr__(self):
        return '<Student %r>' %self.id


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form['button'] == 'create_std':
            
            return redirect('/create_std')
        if request.form['button'] == 'see_std':
            return redirect('/students')
    else:
        return render_template('index.html')

@app.route('/error', methods = ['POST', 'GET'])
def error():
    if request.method == 'POST':
        if request.form['button'] == 'create_std':
            return redirect('/create_std')
        if request.form['button'] == 'see_std':
            return redirect('/students')
    else:  
        return render_template('error.html')

@app.route('/create_std', methods = ['POST', 'GET'])
def create_std():
    if request.method == 'POST':
        name_ = request.form['std_name']
        group_ = request.form['std_group']
        marks_ = request.form['std_marks']

        if marks_.replace(' ', '').isnumeric():
            student = Student(name = name_, group = group_, marks = marks_)
            try: 
                db.session.add(student)
                db.session.commit()
                return redirect('/')
            except Exception as e:
                print(e)
                return redirect('/error')
        else:
            return redirect('/error')
    else:
        return render_template('create_page.html')

@app.route('/students', methods = ['GET', 'POST'])
def students():
    if request.method == 'POST':
        if request.form['button'] == 'return':
            
            return redirect('/')

    else:
        students = Student.query.order_by(Student.name).all()
        return render_template('students.html', students = students)

@app.route('/students/<int:id>', methods = ['GET', 'POST'])
def students_dtl(id):
    if request.method == 'POST':
        if request.form['button'] == 'create_std':
            return redirect('/create_std')
        if request.form['button'] == 'see_std':
            return redirect('/students')


    else:
        student = Student.query.get(id)
        return render_template('student.html', student = student)

if __name__ == "__main__":
    app.run(debug=True)