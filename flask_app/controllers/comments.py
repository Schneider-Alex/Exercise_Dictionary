from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user, exercise, main_group,comment
from flask import flash


@app.route('/createcomment/<int:exerciseid>',methods=['POST'])
def create_exercise_comment(exerciseid):
    if session:
        if comment.Comment.validate_comment(request.form):
            comment.Comment.create_comment(request.form)
        return redirect(f'/exercise/{exerciseid}')
    else:
        flash('must be logged in to create comment!')
        return redirect('/')

@app.route('/createcomment',methods=['POST'])
def create_exercise_comment_ajax():
    print('content route')
    if comment.Comment.validate_comment(request.form):
        print('hello')
        this_comment=comment.Comment.create_comment(request.form)
        print(this_comment)
        return jsonify('hello world')
    else:
        flash('must be logged in to create comment!')
        return redirect(f'/exercise/{request.form["exercise_id"]}')