from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from app.models.debt import Debt
from app.models.customer import Customer
from flask_login import login_required

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/advanced', methods=['GET'])
@login_required
def advanced_search():
    query = request.args.get('query', '')
    category = request.args.get('category', 'all')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    min_amount = request.args.get('min_amount')
    max_amount = request.args.get('max_amount')
    
    if category == 'debt':
        base_query = Debt.query
    elif category == 'customer':
        base_query = Customer.query
    else:
        return jsonify({'error': 'Invalid category'})
        
    if category == 'debt':
        results = base_query.filter(
            or_(
                Debt.description.ilike(f'%{query}%'),
                Customer.name.ilike(f'%{query}%')
            )
        )
        
        if start_date:
            results = results.filter(Debt.start_date >= start_date)
        if end_date:
            results = results.filter(Debt.start_date <= end_date)
        if min_amount:
            results = results.filter(Debt.amount >= float(min_amount))
        if max_amount:
            results = results.filter(Debt.amount <= float(max_amount))
            
    elif category == 'customer':
        results = base_query.filter(
            or_(
                Customer.name.ilike(f'%{query}%'),
                Customer.phone.ilike(f'%{query}%'),
                Customer.email.ilike(f'%{query}%')
            )
        )
    
    return jsonify({
        'results': [item.to_dict() for item in results.all()]
    })