from flask_jwt_extended import JWTManager


jwt = JWTManager()

# Configuration de JWT

def configure_jwt(app):
    app.config['JWT_SECRET_KEY'] = 'votre_clé_secrète'  # Remplacez 'votre_clé_secrète' par une clé secrète forte et sécurisée
    jwt.init_app(app)