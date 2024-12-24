from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # 验证密码是否匹配
        if password != confirm_password:
            flash('密码不匹配')
            return render_template('auth/register.html')
            
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return render_template('auth/register.html')
            
        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册')
            return render_template('auth/register.html')
        
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('注册成功，请登录')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('注册失败，请稍后重试')
            return render_template('auth/register.html')
        
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('debt.index'))
            
        flash('Invalid username or password')
        
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))