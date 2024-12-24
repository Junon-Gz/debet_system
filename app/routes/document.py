import os
from flask import Blueprint, request, current_app, send_from_directory
from werkzeug.utils import secure_filename
from app.models.document import Document
from app import db
from flask_login import login_required
from datetime import datetime
from flask import flash, redirect, url_for

bp = Blueprint('document', __name__, url_prefix='/document')

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload/<int:debt_id>', methods=['POST'])
@login_required
def upload(debt_id):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
        
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 使用债务ID和时间戳创建唯一文件名
        unique_filename = f"{debt_id}_{int(datetime.now().timestamp())}_{filename}"
        
        # 保存文件
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
        
        # 创建文档记录
        doc = Document(
            debt_id=debt_id,
            filename=unique_filename,
            original_filename=filename,
            file_type=filename.rsplit('.', 1)[1].lower()
        )
        db.session.add(doc)
        db.session.commit()
        
        flash('File uploaded successfully')
        return redirect(url_for('debt.detail', id=debt_id)) 