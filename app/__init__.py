from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from app.routes import auth, debt, interest, customer
    app.register_blueprint(auth.bp)
    app.register_blueprint(debt.bp)
    app.register_blueprint(interest.bp) 
    app.register_blueprint(customer.bp)
    
    return app
