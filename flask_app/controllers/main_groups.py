from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user, exercise, main_group
from flask import flash


@app.route('/main/<int:mainid>',methods=['GET'])
def trasnfer_to_main_groups_page(mainid):
    if session:
        return render_template('onemaingroup.html',groups_exercises=main_group.Group.get_one_mains_exercises(mainid))
    else:
        flash('must be logged in to view this page!')
        return redirect('/')


