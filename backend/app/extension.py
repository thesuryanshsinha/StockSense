from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import razorpay
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

client = razorpay.Client(
        auth=(Config.RAZORPAY_KEY_ID, 
        Config.RAZORPAY_KEY_SECRET)
    )