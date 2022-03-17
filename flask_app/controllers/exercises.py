from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user, exercise
from flask import flash

@app.route('/createexercise/<int:mainid>')
def trasnfer_to_create_exercise_page(mainid):
    if session:
        return render_template('newexercisepage.html',mainid=mainid)
    else:
        flash('must be logged in to view this page!')
        return redirect('/')

@app.route('/exercise/<int:mainid>/new',methods=['POST'])
def new_exercise(mainid):
    mainid=mainid
    check=exercise.Exercise.validate_exercise(request.form)
    if check:
        exerciseid=exercise.Exercise.create_exercise(request.form)
        return redirect(f'/exercise/{exerciseid}')
    return redirect(f'/createexercise/{mainid}')

@app.route("/exercise/<int:exerciseid>/like",methods=['POST'])
def like_exercise(exerciseid):
    exercise.Exercise.like_exercise(exerciseid)
    return redirect (f'/exercise/{exerciseid}')

@app.route("/exercise/<int:exerciseid>/unlike",methods=['POST'])
def unlike_exercise(exerciseid):
    exercise.Exercise.unlike_exercise(exerciseid)
    return redirect (f'/exercise/{exerciseid}')


@app.route('/exercise/edit/<int:exerciseid>')
def edit_exercise_page(exerciseid):
    return render_template('edit_exercise_page.html',this_exercise=exercise.Exercise.get_one_exercise(exerciseid))

@app.route('/editexercise',methods=['POST'])
def edit_exercise():
    check=exercise.Exercise.validate_exercise(request.form)
    exerciseid=request.form['id']
    if check:
        exercise.Exercise.update_exercise(request.form)
        return redirect (f'/exercise/{exerciseid}')
    return redirect(f'/exercise/edit/{exerciseid}')

@app.route('/exercise/<int:exerciseid>')
def display_class_detail(exerciseid):
        return render_template('exercise_page.html', this_exercise=exercise.Exercise.get_one_exercise(exerciseid),user_like=exercise.Exercise.get_one_exercises_likes(exerciseid),likes=exercise.Exercise.count_one_exercises_likes(exerciseid),this_exercise_comments=exercise.Exercise.get_one_exercises_comments(exerciseid))

@app.route('/exercise/delete/<int:exerciseid>')
def delete_exercise_link(exerciseid):
    mainid=exercise.Exercise.get_one_exercise(exerciseid).main_group_id
    exercise.Exercise.delete_exercise_and_comments_and_likes(exerciseid)
    return redirect(f'/main/{mainid}')


