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

# @app.route('/saveexercise/<int:mainid>')
# def trasnfer_to_create_exercise_page(mainid):
#     if session:
#         return render_template('newexercisepage.html',mainid=mainid)
#     else:
#         flash('must be logged in to view this page!')
#         return redirect('/')


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


@app.route('/sighting/edit/<int:sightingid>')
def edit_sighting_page(sightingid):
    return render_template('edit_sighting_page.html',this_sighting=sighting.Sighting.get_one_sighting(sightingid))

@app.route('/editsighting',methods=['POST'])
def edit_sighting():
    check=sighting.Sighting.validate_sighting(request.form)
    sightingid=request.form['id']
    if check:
        sighting.Sighting.update_sighting(request.form)
        return redirect ('/dashboard')
    return redirect(f'/sighting/edit/{sightingid}')

@app.route('/exercise/<int:exerciseid>')
def display_class_detail(exerciseid):
        return render_template('exercise_page.html', this_exercise=exercise.Exercise.get_one_exercise(exerciseid),likes=exercise.Exercise.get_one_exercises_likes(exerciseid))

@app.route('/sighting/delete/<int:sightingid>')
def delete_sighting_link(sightingid):
    sighting.Sighting.delete_sighting(sightingid)
    return redirect('/dashboard')


