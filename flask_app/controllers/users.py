from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user, exercise, main_group
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/createuser', methods=['POST'])
def add_user():
    check=user.User.validate_user(request.form)
    print(check)
    print('hello')
    if check:
        user.User.create_user(request.form)
        logged_in_user=user.User.login_user(request.form)
        print(session['id'])
        return redirect('/dashboard')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    logged_in_user=user.User.login_user(request.form)
    if logged_in_user:
        return redirect("/dashboard")
    return redirect ('/')


@app.route ('/dashboard')
def dashboardpage():
    return render_template('dashboard.html',groups=main_group.Group.get_all_main_groups())

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')
