from flask_apscheduler import APScheduler
from app import create_app, db
from app.models.debt import Debt
from app.models.interest import Interest
from datetime import datetime, timedelta
from app.utils.email import send_email

scheduler = APScheduler()

@scheduler.task('cron', id='check_overdue', hour=0)
def check_overdue():
    """每天检查逾期债务并发送提醒"""
    with create_app().app_context():
        overdue_debts = Debt.query.filter(
            Debt.end_date < datetime.now(),
            Debt.status == 'active'
        ).all()
        
        for debt in overdue_debts:
            send_email(
                to=debt.customer.email,
                subject='债务逾期提醒',
                template='email/overdue_notice',
                debt=debt
            )

@scheduler.task('cron', id='calculate_monthly_interest', day=1, hour=0)
def calculate_monthly_interest():
    """每月1号计算上月利息"""
    with create_app().app_context():
        last_month = datetime.now().replace(day=1) - timedelta(days=1)
        active_debts = Debt.query.filter_by(status='active').all()
        
        for debt in active_debts:
            # 计算月利息
            monthly_interest = debt.amount * (debt.interest_rate / 100 / 12)
            
            interest = Interest(
                debt_id=debt.id,
                amount=monthly_interest,
                period_start=last_month.replace(day=1),
                period_end=last_month
            )
            db.session.add(interest)
        
        db.session.commit() 