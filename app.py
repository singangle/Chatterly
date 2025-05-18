from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = '1145141919810'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://LiuZianAnderson:1145141919810@localhost/chatdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    messages = db.relationship('Message', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/join', methods=['POST'])
def join():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember') == 'on'

    # Email validation
    # 更严格的邮箱验证规则
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$', email):
        return render_template('home.html', email_error=True)
    
    # 添加邮箱长度限制
    if len(email) > 254:
        return render_template('home.html', email_error=True)

    # Password validation
    if len(password) < 6 or not re.search(r'\d', password) or not re.search(r'[a-zA-Z]', password):
        return render_template('home.html', password_error=True)

    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            response = redirect(url_for('chat'))
            if remember:
                response.set_cookie(
                    'remember_token',
                    str(user.id),
                    max_age=30*24*60*60,
                    httponly=True
                )
            return response
        elif not user:
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            response = redirect(url_for('chat'))
            if remember:
                response.set_cookie(
                    'remember_token',
                    str(user.id),
                    max_age=30*24*60*60,
                    httponly=True
                )
            return response
        else:
            return render_template('home.html', email_registered_error=True)
    return redirect(url_for('home'))

@app.before_request
def check_remembered_user():
    # 跳过静态文件、首页、登录、注册、endpoint为None的请求
    skip_endpoints = ['static', 'home', 'join']
    if request.endpoint is None or request.endpoint in skip_endpoints:
        return

    # 已登录直接放行
    if 'user_id' in session:
        return

    # 检查cookie
    remember_token = request.cookies.get('remember_token')
    if remember_token:
        try:
            user_id = int(remember_token)
            user = User.query.get(user_id)
            if user:
                session['user_id'] = user.id
                return
        except Exception:
            pass
    # 未登录且无有效cookie，重定向到首页
    return redirect(url_for('home'))

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    messages = Message.query.order_by(Message.timestamp.desc()).limit(50).all()
    return render_template('chat.html', messages=messages)

@app.route('/send', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    content = request.form.get('message')
    if content:
        message = Message(content=content, user_id=session['user_id'])
        db.session.add(message)
        db.session.commit()
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run(debug=True)