from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.job import Job
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/loginPage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('LogReg.html')


@app.route('/register', methods=['POST'])
def createUser():
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    if User.get_user_by_email(request.form):
        flash('This email already exists!', 'emailSignUp')
        return redirect(request.referrer)
    data = {
        'email': request.form['email'],
        'name': request.form['name'],
        'lastName': request.form['lastName'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.create_user(data)
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    if len(request.form['email'])<1:
        flash('Email is required to login', 'emailLogin')
        return redirect(request.referrer)

    if not User.get_user_by_email(data):
        flash('This email doesnt exist ', 'emailLogin')
        return redirect(request.referrer)
    user = User.get_user_by_email(data)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Invalid Password", 'passwordLogin')
        return redirect(request.referrer) 
    session['user_id'] = user['id']
    return redirect('/')



@app.route('/')
def dashboard():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
            
        }
        user= User.get_user_by_id(data)
        myjob=Job.get_user_job(data)
        addedJobs = Job.get_user_added_job(data)
        jobs=Job.get_all_jobs()
        return render_template('dashboard.html',loginUser=user, myjob=myjob, jobs=jobs,addedJobs=addedJobs)
    return redirect('/logout')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginPage')

