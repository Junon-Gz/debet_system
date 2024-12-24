from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.interest import Interest
from app.models.debt import Debt
from app import db
from datetime import datetime

bp = Blueprint('interest', __name__, url_prefix='/interest')

@bp.route('/')
@login_required
def index():
    interests = Interest.query.all()
    return render_template('interest/index.html', interests=interests)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        interest = Interest(
            debt_id=request.form['debt_id'],
            amount=float(request.form['amount']),
            period_start=datetime.strptime(request.form['period_start'], '%Y-%m-%d'),
            period_end=datetime.strptime(request.form['period_end'], '%Y-%m-%d')
        )
        db.session.add(interest)
        db.session.commit()
        return redirect(url_for('interest.index'))
        
    debts = Debt.query.filter_by(status='active').all()
    return render_template('interest/create.html', debts=debts) 

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    interest = Interest.query.get_or_404(id)
    
    if request.method == 'POST':
        interest.amount = float(request.form['amount'])
        interest.period_start = datetime.strptime(request.form['period_start'], '%Y-%m-%d')
        interest.period_end = datetime.strptime(request.form['period_end'], '%Y-%m-%d')
        
        db.session.commit()
        flash('利息记录已更新')
        return redirect(url_for('interest.index'))
        
    debts = Debt.query.filter_by(status='active').all()
    return render_template('interest/edit.html', interest=interest, debts=debts) 