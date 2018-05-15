from flask import Flask, render_template, redirect, request, jsonify, url_for, send_from_directory, \
    render_template_string, json
from flask_login import login_user, UserMixin, login_required, logout_user, current_user, LoginManager
import logging.config
from os import path
from models import Member, Task
from utils import FlashUtils, UploadUtils, PasswordUtils, send_email, DbQuery
import time



login_manager = LoginManager()
login_manager.login_view = "login_page"
login_manager.login_message = u"Пожалуйста, авторизуйтесь."
login_manager.login_message_category = "info"

app = Flask(__name__)
login_manager.init_app(app)
app.config.from_object('config.ProductionConfig') #uncommentfor production
# app.config.from_object('config.SandboxConfig')

db_query = DbQuery()


@login_manager.user_loader
def load_user(user_id):
    member = Member(id=user_id)
    try:
        member.get()
    except:
        logout_user()
    return member

@app.route('/login', methods=('POST', 'GET'))
def login_page():
    if request.method == 'POST':
        try:
            member = Member(id=request.form.get('id', ' '))
            member.get()
            print(member)
        except Exception:
            return render_template('login.html')
        if member.password == request.form.get('password', ' '):
            login_user(member, remember=True)
            if member.status == 0:
                member.update_status(1)
            return redirect('/search')
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/index', methods=('POST', 'GET'))
def main_page():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/search', methods=('POST', 'GET'))
def search():
    if current_user.status == 2:
        return redirect('/index')
    return render_template('search.html')

@app.route('/search_member', methods=('POST', 'GET'))
def search_member():
    member = Member(id = current_user.id)
    member.get()
    if current_user.status == 2:
        return json.dumps({'result': 'Found a partner! Refresh page to continue.'})
    if member.search():
        return json.dumps({'result': 'Found!'})
    else:
        return json.dumps({'result': 'Searching for partner...' })


@app.route('/get_len', methods=['GET', 'POST'])
def get_len():
    name = request.form['name']
    member = Member(id=name)
    member.get()
    return json.dumps({'len': len(name), 'user': member.password})


@app.route('/time', methods=['GET', 'POST'])
def time():
    return json.dumps({'result': 'none'})


@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    member = Member(id=current_user.id)
    member.get()
    task = Task(id=member.task_id)
    if member.team_status() == 3:
        member.update_task(member.task_id+2)
        member.update_answer('')
        member.update_status(2)

    task.get()
    mate_answer = member.get_answer()
    mate_task = member.get_task()

    return json.dumps({'task': task.value, 'mate_task': mate_task, 'mate_answer': mate_answer})

@app.route('/send', methods=['GET', 'POST'])
def send():
    member = Member(id=current_user.id)
    member.get()
    member.update_answer(request.form.get('answer', ' '))
    return json.dumps({'result': 'none'})

@app.route('/check', methods=['GET', 'POST'])
def check():
    member = Member(id=current_user.id)
    member.get()
    member.update_status(3)
    return json.dumps({'result': 'none'})



#
# @socketio.on('join')
# def submit(message):
#     join_room(str(current_user.id+'_task'))
#     join_room(str(current_user.id+'_check'))
#     join_room('chat')
#     print(111)
#     emit('Success', room=str(current_user.id+'_task'))
#     emit('Success', room=str(current_user.id + '_check'))
#     emit('Success', room='chat')
#







# @socketio.on('join')
# def on_join(data):
#     username = data['username']
#     room = data['room']
#     join_room(room)
#     send(username + ' has entered the room.', room=room)


if __name__ == '__main__':
    app.run(debug=True)