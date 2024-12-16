from flask import Flask, render_template, abort, send_from_directory
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

    if test_config:
        app.config.update(test_config)

    freezer = Freezer(app)
    note_generator = NoteGenerator(app.config['CONTENT_DIR'])

    @app.context_processor
    def utility_processor():
        return {
            'current_year': datetime.now().year,
            'categories': note_generator.get_categories(),
            'site_name': 'Study Notes'
        }

    @app.route('/')
    def index():
        categories = note_generator.get_categories()
        recent_notes = note_generator.get_all_notes()[:5]
        return render_template('index.html',
                            categories=categories,
                            recent_notes=recent_notes)

    @app.route('/<path:note_path>')
    def note(note_path):
        note_data = note_generator.get_note_by_url(note_path)
        if note_data is None:
            abort(404)
        return render_template('note.html', note=note_data)

    @app.route('/category/<category>')
    def category(category):
        categories = note_generator.get_categories()
        if category not in categories:
            abort(404)
        return render_template('index.html',
                            categories={category: categories[category]},
                            category_name=category)

    @freezer.register_generator
    def note_url_generator():
        for note in note_generator.get_all_notes():
            yield 'note', {'note_path': note['url'].lstrip('/')}

    @freezer.register_generator
    def category_url_generator():
        for category in note_generator.get_categories():
            yield 'category', {'category': category}

    return app, freezer

app, freezer = create_app()

if __name__ == '__main__':
    app.run()