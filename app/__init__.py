from flask import Flask, redirect, url_for
from .config import Config
from flask_cors import CORS
from .extension import db, migrate, bcrypt, login_manager

def create_app():

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    CORS(
    app,
    resources={r"/*": {"origins": "http://localhost:5173"}},
    supports_credentials=True
    )
    
    with app.app_context():

        db.create_all()
        db.session.commit()

    from app.auth.routes import auth_bp
    from app.dashboard.manager.routes import m_dash
    from app.dashboard.staff.routes import s_dash
    app.register_blueprint(auth_bp)
    app.register_blueprint(m_dash)
    app.register_blueprint(s_dash)
    @app.errorhandler(401)
    @app.errorhandler(404)
    def unauthorised_access_or_page_unavailable(_):
        return redirect(url_for('auth.login')) 
    
    @app.errorhandler(403)
    def wrong_dashboard(_):
        return redirect(url_for('dash.dashboard'))
    
    # for rule in app.url_map.iter_rules():
    #     print(rule.endpoint, rule)

    return app