from flask import Flask
from flask_migrate import Migrate
from app.extensions import db
from dotenv import load_dotenv
import os
from flask_migrate import upgrade

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'   
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 

    db.init_app(app)

    Migrate(app, db) #flask db init #flask db migrate -m "name here" #flask db upgrade

    
    # Ensure the database directory exists and run migrations
    with app.app_context():
        if not os.path.exists(os.path.join(app.instance_path, 'db')):
            os.makedirs(os.path.join(app.instance_path, 'db'))
        upgrade()

    # Import and register blueprints
    from .routes.main import main_blueprint
    from .routes.settings import settings_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(settings_blueprint)

    return app