# models/__init__.py

import os
import importlib

# Obtenez le nom de votre package (dossier) de modèles
package_name = os.path.basename(os.path.dirname(__file__))

# Liste des fichiers .py dans le dossier des modèles
model_files = [
    filename[:-3] for filename in os.listdir(os.path.dirname(__file__)) if filename.endswith('.py') and filename != '__init__.py' and filename != 'test.py'
]

# Importez dynamiquement tous les modèles
models = {}
for model_file in model_files:
    model_module = importlib.import_module(f'{package_name}.{model_file}')
    models[model_file] = getattr(model_module, model_file)

# Vous pouvez maintenant accéder à tous les modèles en utilisant le dictionnaire "models"

import models.relations
