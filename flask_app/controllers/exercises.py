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


@app.route('/exercise/new',methods=['POST'])
def new_exercise():
    check=exercise.Exercise.validate_exercise(request.form)
    if check:
        sighting.Sighting.create_sighting(request.form)
        return redirect('/dashboard')
    return redirect(f'createexercise/{mainid}')

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

@app.route('/sighting/<int:sightingid>')
def display_class_detail(sightingid):
        return render_template('sighting_page.html', this_sighting=sighting.Sighting.get_one_sighting(sightingid))

@app.route('/sighting/delete/<int:sightingid>')
def delete_sighting_link(sightingid):
    sighting.Sighting.delete_sighting(sightingid)
    return redirect('/dashboard')


