from flask_app import app
from flask import render_template,redirect,request,session,flash, jsonify
from flask_app.models import user, exercise, main_group,comment

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
        comment_object=comment.Comment.get_one_comments_author(this_comment)
        comment_dict={
                "id" : comment_object.id,
                "content" : comment_object.content,
                "written_by" : comment_object.written_by,
                "written_for" : comment_object.written_for
        }
        return jsonify(comment_dict)
    else:
        flash('must be logged in to create comment!')
        return redirect(f'/exercise/{request.form["exercise_id"]}')
