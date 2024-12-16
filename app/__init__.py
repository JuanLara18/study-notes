from flask import Flask, render_template
from flask_frozen import Freezer
from datetime import datetime
import os

from .generator import NoteGenerator

def create_app(test_config=None):
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        FREEZER_DESTINATION=os.path.abspath(os.path.join(app.root_path, '..', 'build')),
        FREEZER_RELATIVE_URLS=True,
        CONTENT_DIR=os.path.abspath(os.path.join(app.root_path, '..', 'content')),
    )

    freezer = Freezer(app)
    note_generator = NoteGenerator(app.config['CONTENT_DIR'])

    @app.context_processor
    def utility_processor():
        return {
            'current_year': datetime.now().year,
            'site_name': 'Study Notes'
        }

    @app.route('/')
    def index():
        notes = note_generator.get_all_notes()
        return render_template('index.html', notes=notes)

    @freezer.register_generator
    def index_url_generator():
        yield 'index', {}

    return app, freezer

app, freezer = create_app()