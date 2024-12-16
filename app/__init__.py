from flask import Flask, render_template, abort, send_from_directory
from flask_frozen import Freezer
from datetime import datetime
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .generator import NoteGenerator, ContentValidationError

def configure_logging(app):
    """Configure application logging with rotation and formatting."""
    if not os.path.exists('logs'):
        os.mkdir('logs')
        
    file_handler = RotatingFileHandler(
        'logs/study_notes.log', 
        maxBytes=10240, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Study Notes startup')

def create_app(test_config=None):
    """Application factory function."""
    app = Flask(__name__)
    
    # Default Configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        FREEZER_DESTINATION=os.path.abspath(os.path.join(app.root_path, '..', 'build')),
        FREEZER_RELATIVE_URLS=True,
        CONTENT_DIR=os.path.abspath(os.path.join(app.root_path, '..', 'content')),
        GITHUB_REPO='https://github.com/yourusername/study-notes',
        ENABLE_COMMENTS=False,
        MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16MB max file size
    )

    if test_config is None:
        # Load the instance config, if it exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Configure logging
    configure_logging(app)

    # Initialize Frozen-Flask
    freezer = Freezer(app)
    
    # Initialize the note generator
    try:
        note_generator = NoteGenerator(app.config['CONTENT_DIR'])
    except Exception as e:
        app.logger.error(f"Failed to initialize NoteGenerator: {str(e)}")
        raise

    @app.context_processor
    def utility_processor():
        """Make common variables available to all templates."""
        return {
            'current_year': datetime.now().year,
            'categories': note_generator.get_categories(),
            'site_name': 'Study Notes',
            'github_repo': app.config['GITHUB_REPO']
        }

    @app.route('/favicon.ico')
    def favicon():
        """Serve favicon from static directory."""
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico', 
            mimetype='image/vnd.microsoft.icon'
        )

    @app.route('/')
    def index():
        """Render the home page."""
        try:
            categories = note_generator.get_categories()
            recent_notes = note_generator.get_all_notes()[:5]
            tags = {tag: len(notes) for tag, notes in note_generator.get_tags().items()}
            return render_template('index.html',
                                categories=categories,
                                recent_notes=recent_notes,
                                tags=tags)
        except Exception as e:
            app.logger.error(f"Error rendering index: {str(e)}")
            abort(500)

    @app.route('/<path:note_path>')
    def note(note_path):
        """Render individual note pages."""
        try:
            note_data = note_generator.get_note_by_url(note_path)
            if note_data is None:
                abort(404)
            
            # Get related notes
            related_notes = note_generator.get_related_notes(note_data)
            
            # Get navigation links
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
        except ContentValidationError as e:
            app.logger.error(f"Content validation error for {note_path}: {str(e)}")
            abort(500)
        except Exception as e:
            app.logger.error(f"Error rendering note {note_path}: {str(e)}")
            abort(500)

    @app.route('/category/<category>')
    def category(category):
        """Render category pages."""
        try:
            categories = note_generator.get_categories()
            if category not in categories:
                abort(404)
            
            return render_template('index.html',
                                categories={category: categories[category]},
                                category_name=category)
        except Exception as e:
            app.logger.error(f"Error rendering category {category}: {str(e)}")
            abort(500)

    @app.route('/tag/<tag>')
    def tag(tag):
        """Render tag pages."""
        try:
            tags = note_generator.get_tags()
            if tag not in tags:
                abort(404)
            
            return render_template('index.html',
                                categories={'Tagged: ' + tag: tags[tag]},
                                tag_name=tag)
        except Exception as e:
            app.logger.error(f"Error rendering tag {tag}: {str(e)}")
            abort(500)

    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors."""
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return render_template('errors/500.html'), 500

    @freezer.register_generator
    def note_url_generator():
        """Generate URLs for freezing note pages."""
        for note in note_generator.get_all_notes():
            yield 'note', {'note_path': note['url'].lstrip('/')}

    @freezer.register_generator
    def category_url_generator():
        """Generate URLs for freezing category pages."""
        for category in note_generator.get_categories():
            yield 'category', {'category': category}

    @freezer.register_generator
    def tag_url_generator():
        """Generate URLs for freezing tag pages."""
        for tag in note_generator.get_tags():
            yield 'tag', {'tag': tag}
            
    @freezer.register_generator
    def favicon_url_generator():
        yield 'favicon', {}

    return app, freezer

# Create the application instance
app, freezer = create_app()

if __name__ == '__main__':
    app.run()