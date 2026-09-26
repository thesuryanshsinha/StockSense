from flask import Flask, redirect, url_for
# from .db.models import *
from .config import Config
from .extension import db, migrate, bcrypt, login_manager

def create_app():

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # with app.app_context():

        # db.create_all()
        # db.session.commit()

        # user =  Users.query.filter_by(email='admin@gmail.com').first()

        # if not user:
        #     password = bcrypt.generate_password_hash('test')
        #     db.session.add(Users(user_id=1,name='Admin',role='admin',email='admin@gmail.com',password=password))
        #     scripts = ["app/db/triggers_and_fts.sql","app/db/dummy_data.sql"]
        #     # scripts = ["app/db/dummy_data.sql"]
        #     for i in scripts:
        #         with open(i,'r') as f:
        #             sql = f.read()
        #             conn = db.engine.raw_connection()
        #             conn.executescript(sql)
        #             conn.commit()

        #         db.session.commit()

    # from app.auth.routes import auth_bp
    # from app.api.bookings import bookings_api
    # from app.api.users import users_api
    # from app.api.treks import treks_api
    # from app.dashboard.dashboard import dash_bp
    # from app.dashboard.admin_dashboard import admin_bp
    # from app.dashboard.staff_dashboard import staff_bp
    # from app.dashboard.trekker_dashboard import trekker_bp

    # app.register_blueprint(auth_bp)
    # app.register_blueprint(dash_bp, url_prefix='/dashboard')
    # app.register_blueprint(admin_bp, url_prefix='/dashboard/admin')
    # app.register_blueprint(staff_bp, url_prefix='/dashboard/staff')
    # app.register_blueprint(trekker_bp, url_prefix='/dashboard/trekker')

    # app.register_blueprint(bookings_api, url_prefix='/api/bookings')
    # app.register_blueprint(users_api, url_prefix='/api/users')
    # app.register_blueprint(treks_api, url_prefix='/api/treks')

    # @app.errorhandler(401)
    # @app.errorhandler(404)
    # def unauthorised_access_or_page_unavailable(_):
    #     return redirect(url_for('auth.login')) 
    
    # @app.errorhandler(403)
    # def wrong_dashboard(_):
    #     return redirect(url_for('dash.dashboard'))
    
    # for rule in app.url_map.iter_rules():
    #     print(rule.endpoint, rule)

    return app