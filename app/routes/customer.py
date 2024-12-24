from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.customer import Customer
from app import db

bp = Blueprint('customer', __name__, url_prefix='/customer')

@bp.route('/')
@login_required
def index():
    customers = Customer.query.all()
    return render_template('customer/index.html', customers=customers)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        customer = Customer(
            name=request.form['name'],
            phone=request.form['phone'],
            email=request.form['email'],
            address=request.form['address'],
            id_number=request.form['id_number']
        )
        db.session.add(customer)
        db.session.commit()
        flash('客户创建成功')
        return redirect(url_for('customer.index'))
        
    return render_template('customer/create.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.phone = request.form['phone']
        customer.email = request.form['email']
        customer.address = request.form['address']
        customer.id_number = request.form['id_number']
        
        db.session.commit()
        flash('客户信息已更新')
        return redirect(url_for('customer.index'))
        
    return render_template('customer/edit.html', customer=customer) 