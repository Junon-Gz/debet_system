from flask import Blueprint, render_template
from flask_login import login_required
from app.models.debt import Debt
from app.models.interest import Interest
from sqlalchemy import func
from datetime import datetime, timedelta
from app import db

bp = Blueprint('statistics', __name__, url_prefix='/statistics')

@bp.route('/')
@login_required
def index():
    # 获取总债务金额
    total_debt = db.session.query(func.sum(Debt.amount)).scalar() or 0
    
    # 获取本月利息收入
    start_of_month = datetime.now().replace(day=1)
    month_interest = db.session.query(func.sum(Interest.amount))\
        .filter(Interest.payment_date >= start_of_month).scalar() or 0
    
    # 获取逾期债务数量
    overdue_count = Debt.query.filter(
        Debt.end_date < datetime.now(),
        Debt.status == 'active'
    ).count()
    
    # 按月统计利息收入
    monthly_stats = db.session.query(
        func.strftime('%Y-%m', Interest.payment_date).label('month'),
        func.sum(Interest.amount).label('total')
    ).group_by('month').all()
    
    return render_template('statistics/index.html',
                         total_debt=total_debt,
                         month_interest=month_interest,
                         overdue_count=overdue_count,
                         monthly_stats=monthly_stats) 