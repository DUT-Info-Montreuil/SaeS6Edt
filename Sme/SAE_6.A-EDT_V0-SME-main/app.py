from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from routes import register_routes
from database import configure_database,insert_data, db
from utils.jwt import configure_jwt, jwt 

from flask_cors import CORS



load_dotenv()

def create_app():

    app = Flask(__name__)

    configure_database(app)
    configure_jwt(app)

    migrate = Migrate(app, db)
    app.debug = True

    CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})    
    register_routes(app)

    return app

app = create_app()



with app.app_context():
    db.drop_all()
    db.create_all()
    insert_data()

    
if __name__ == '__main__':
    app.run()