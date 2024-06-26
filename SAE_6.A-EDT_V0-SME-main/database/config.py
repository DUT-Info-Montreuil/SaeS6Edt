from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

# Configuration de la base de données
# DB_URI = os.environ.get('DATABASE_URL')

def configure_database(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

def insert_data():
    import database.scripts

def drop_admin():
    from models.ResponsableEdt import ResponsableEdt
    admin = ResponsableEdt.query.filter_by(username='admin').first()
    db.session.delete(admin)

    db.session.commit()