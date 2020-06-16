import os
from flask import Flask, render_template
from pathlib import Path
from dotenv import load_dotenv
from flask_cors import CORS
from .models.models import setup_db

# Set env directory
env_folder = Path(Path(__file__).parent).parent
env_file = os.path.join(env_folder, '.env')
load_dotenv(dotenv_path=env_file)


def create_app():
    # Create app
    app = Flask(__name__, static_folder="frontend/static", template_folder="frontend")

    # Setup Database
    setup_db(app)

    # Setup CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS,PATCH')

        return response

    from .TODO.routes import todo
    from .errors.handlers import errors

    app.register_blueprint(todo)
    app.register_blueprint(errors)

    @app.route('/')
    def index():
    	return render_template('index.html')

    return app
