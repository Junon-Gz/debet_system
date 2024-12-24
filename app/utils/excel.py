import pandas as pd
from io import BytesIO
from datetime import datetime

def export_debts_to_excel(debts):
    """导出债务数据到Excel"""
    data = []
    for debt in debts:
        data.append({
            '债务ID': debt.id,
            '客户姓名': debt.customer.name,
            '金额': debt.amount,
            '利率': debt.interest_rate,
            '开始日期': debt.start_date,
            '结束日期': debt.end_date,
            '状态': debt.status,
            '描述': debt.description
        })
    
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='债务列表', index=False)
    
    output.seek(0)
    return output

def export_customers_to_excel(customers):
    """导出客户数据到Excel"""
    data = []
    for customer in customers:
        data.append({
            '客户ID': customer.id,
            '姓名': customer.name,
            '电话': customer.phone,
            '邮箱': customer.email,
            '地址': customer.address,
            '身份证号': customer.id_number
        })
    
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='客户列表', index=False)
    
    output.seek(0)
    return output 