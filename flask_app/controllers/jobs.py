from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.job import Job
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/addjob')
def addJob():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id']
    }
    loginUser=User.get_user_by_id(data)
    return render_template('addjob.html',loginUser=loginUser)

@app.route('/create_job', methods=['POST'])
def createJob():
    if not Job.validate_job(request.form):
        return redirect(request.referrer)

    Job.create_job(request.form)
    return redirect('/')



@app.route('/edit/<int:id>')
def editForm(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
            'job_id': id,
            'user_id': session['user_id']
        }
    job = Job.get_job_by_id(data)
    loginUser=User.get_user_by_id(data)
    if not session['user_id'] == job['user_id']:
        return redirect('/dashboard')
    return render_template('edit.html', loginUser=loginUser, job=job)


@app.route('/update/<int:id>', methods = ['POST'])
def updateJob(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Job.validate_job(request.form):
        return redirect(request.referrer)

    job = Job.get_job_by_id(request.form)
    
    if not session['user_id'] == job['user_id']:
        return redirect('/dashboard')
    Job.update_job(request.form)

    return redirect('/')


@app.route('/view/<int:id>')
def viewJob(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
            'job_id': id,
            'user_id': session['user_id']
        }
    job = Job.get_job_by_id(data)
    loginUser=User.get_user_by_id(data)
    Jobcreator = Job.get_user_job(data)
    jobIds = Job.get_user_added_jobIds(data)
    return render_template('view.html', loginUser=loginUser, job=job, Jobcreator=Jobcreator, jobIds=jobIds)


@app.route('/add/<int:id>')
def addtomyJob(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        'job_id': id,
        'user_id': session['user_id']
        }
    Job.addMyJob(data)
    return redirect(request.referrer)


@app.route('/cancel/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'job_id': id,
        'user_id': session['user_id']
    }
    job = Job.get_job_by_id(data)

    if not session['user_id'] == job['user_id']:
        return redirect('/dashboard')
    Job.delete(data)
    return redirect(request.referrer)