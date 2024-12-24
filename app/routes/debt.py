from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.debt import Debt
from app.models.customer import Customer
from app import db

bp = Blueprint('debt', __name__, url_prefix='/debt')

@bp.route('/')
@login_required
def index():
    debts = Debt.query.all()
    return render_template('debt/index.html', debts=debts)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        debt = Debt(
            customer_id=request.form['customer_id'],
            amount=float(request.form['amount']),
            interest_rate=float(request.form['interest_rate']),
            description=request.form.get('description')
        )
        db.session.add(debt)
        db.session.commit()
        flash('债务创建成功')
        return redirect(url_for('debt.index'))
        
    customers = Customer.query.all()
    return render_template('debt/create.html', customers=customers)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    debt = Debt.query.get_or_404(id)
    
    if request.method == 'POST':
        debt.customer_id = request.form['customer_id']
        debt.amount = float(request.form['amount'])
        debt.interest_rate = float(request.form['interest_rate'])
        debt.description = request.form.get('description')
        
        db.session.commit()
        flash('债务信息已更新')
        return redirect(url_for('debt.index'))
        
    customers = Customer.query.all()
    return render_template('debt/edit.html', debt=debt, customers=customers) 