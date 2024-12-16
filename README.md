# Study Notes Generator

A static site generator built with Flask designed specifically for academic study notes. This project helps you create and maintain a collection of academic notes with support for mathematics equations, code snippets, and a clean, responsive design.

## Features

### Content Management
- Markdown-based content creation with YAML front matter
- Support for mathematical equations using KaTeX
- Code syntax highlighting with Pygments
- Organized content structure by categories (Mathematics, Computer Science, Economics)
- Tag-based organization and filtering
- Automatic generation of related notes based on categories and tags

### User Interface
- Clean, responsive design optimized for readability
- Dark/light theme support
- Category-based navigation
- Tag cloud for easy content discovery
- Mobile-friendly layout
- Printer-friendly styles

### Technical Features
- Built with Flask and Frozen-Flask for static site generation
- KaTeX integration for mathematical equations
- Code syntax highlighting
- Support for tables and other Markdown extensions
- Custom metadata processing
- Search functionality
- Related content suggestions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/study-notes.git
cd study-notes
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Adding Content

Create your notes as Markdown files in the `content` directory. Each note should include YAML front matter with the following metadata:

```markdown
---
title: "Your Note Title"
date: 2024-01-01
category: mathematics
tags: [calculus, derivatives, applications]
author: Your Name (optional)
---

Your note content here...
```

Organize your notes in the appropriate category subdirectory:
- `content/mathematics/`
- `content/computer-science/`
- `content/economics/`

### Writing Mathematics

Use KaTeX syntax for mathematical equations:

- Inline equations: `$E = mc^2$`
- Display equations: 
```
$$
\frac{d}{dx}(x^n) = nx^{n-1}
$$
```

### Code Snippets

Use fenced code blocks with language specification:

````markdown
```python
def hello_world():
    print("Hello, World!")
```
````

### Development Server

To run the development server:

```bash
flask --app app run --debug
```

### Building Static Site

To generate the static site:

```bash
flask --app app freeze
```

The static site will be generated in the `build` directory.

## Configuration

Edit `app/__init__.py` to configure:

- `GITHUB_REPO`: Your GitHub repository URL
- `ENABLE_COMMENTS`: Enable/disable comments section
- Other Flask configuration options

## Project Structure

```
study-notes/
├── README.md
├── requirements.txt
├── content/               # Your Markdown notes
│   ├── mathematics/
│   ├── computer-science/
│   └── economics/
├── app/
│   ├── __init__.py       # Flask application
│   ├── templates/        # Jinja2 templates
│   ├── static/          # CSS, JS, and images
│   └── generator.py     # Note processing logic
└── build/               # Generated static site
```

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Mathematics rendering by [KaTeX](https://katex.org/)
- Code syntax highlighting by [Pygments](https://pygments.org/)