from flask import Flask, render_template, abort
from flask_frozen import Freezer
from datetime import datetime
import os

from .generator import NoteGenerator

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Configuración básica
    app.config.from_mapping(
        SECRET_KEY='dev',
        FREEZER_DESTINATION='../build',
        FREEZER_RELATIVE_URLS=True,
        GITHUB_REPO='https://github.com/yourusername/study-notes',
        ENABLE_COMMENTS=False
    )

    if test_config is None:
        # Cargar configuración de instancia si existe
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Cargar configuración de prueba
        app.config.update(test_config)

    # Asegurar que existe el directorio de contenido
    try:
        os.makedirs(os.path.join(app.instance_path, 'content'))
    except OSError:
        pass

    # Inicializar el generador de notas
    note_generator = NoteGenerator('content')
    freezer = Freezer(app)

    @app.context_processor
    def utility_processor():
        return {
            'current_year': datetime.now().year,
            'categories': note_generator.get_categories().keys()
        }

    @app.route('/')
    def index():
        categories = note_generator.get_categories()
        recent_notes = note_generator.get_all_notes()[:5]
        tags = {tag: len(notes) for tag, notes in note_generator.get_tags().items()}
        return render_template('index.html', 
                             categories=categories,
                             recent_notes=recent_notes,
                             tags=tags)

    @app.route('/<path:note_path>')
    def note(note_path):
        note_data = note_generator.get_note_by_url(note_path)
        if note_data is None:
            abort(404)
            
        # Obtener notas relacionadas
        related_notes = note_generator.get_related_notes(note_data)
        
        # Obtener notas anterior y siguiente
        all_notes = note_generator.get_all_notes()
        current_index = next((i for i, note in enumerate(all_notes) 
                            if note['url'] == note_data['url']), None)
        
        prev_note = all_notes[current_index - 1] if current_index > 0 else None
        next_note = (all_notes[current_index + 1] 
                    if current_index < len(all_notes) - 1 else None)

        return render_template('note.html',
                             note=note_data,
                             related_notes=related_notes,
                             prev_note=prev_note,
                             next_note=next_note)

    @app.route('/category/<category>')
    def category(category):
        categories = note_generator.get_categories()
        if category not in categories:
            abort(404)
            
        return render_template('index.html',
                             categories={category: categories[category]},
                             category_name=category)

    @app.route('/tag/<tag>')
    def tag(tag):
        tags = note_generator.get_tags()
        if tag not in tags:
            abort(404)
            
        return render_template('index.html',
                             categories={'Tagged: ' + tag: tags[tag]},
                             tag_name=tag)

    @freezer.register_generator
    def note_url_generator():
        for note in note_generator.get_all_notes():
            yield 'note', {'note_path': note['url'].lstrip('/')}

    @freezer.register_generator
    def category_url_generator():
        for category in note_generator.get_categories():
            yield 'category', {'category': category}

    @freezer.register_generator
    def tag_url_generator():
        for tag in note_generator.get_tags():
            yield 'tag', {'tag': tag}

    return app