# Study Notes Platform

A sophisticated static site generator built with Flask, specifically designed for creating and managing academic study notes. This platform offers comprehensive support for mathematical equations, code snippets, syntax highlighting, and a responsive design optimized for learning.

## Core Features

The Study Notes Platform provides a robust set of features designed to enhance the learning experience:

### Content Management
The platform offers flexible content creation and organization capabilities:

- Markdown-based authoring with YAML front matter for metadata
- Full mathematical equation support through KaTeX integration
- Code syntax highlighting powered by Pygments
- Hierarchical content organization by academic disciplines
- Intelligent tag-based content discovery
- Automated related content suggestions based on categories and tags
- Full-text search functionality

### User Interface
The interface is designed for optimal readability and usability:

- Clean, minimalist design focused on content
- Seamless dark/light theme switching
- Dynamic category-based navigation system
- Interactive tag cloud for content exploration
- Fully responsive layout for all devices
- Print-optimized styling for physical copies
- Table of contents generation for long-form content
- Breadcrumb navigation for clear content hierarchy

### Technical Architecture
Built on modern web technologies:

- Flask framework for robust backend processing
- Frozen-Flask for static site generation
- KaTeX for high-quality mathematical typesetting
- Pygments for advanced code highlighting
- Advanced metadata processing system
- Automated deployment to GitHub Pages
- Custom templating system for consistent styling

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Git (for version control)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/study-notes.git
cd study-notes
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Content Creation

Create your study notes using Markdown files in the `content` directory. Each note requires YAML front matter with the following structure:

```markdown
---
title: "Your Note Title"
date: 2024-01-01
category: mathematics
tags: [calculus, derivatives, analysis]
author: Your Name
---

Your note content here...
```

### Directory Structure

The platform follows a well-organized directory structure:

```
study-notes/
├── app/
│   ├── static/          # Static assets (CSS, JS, images)
│   ├── templates/       # Jinja2 template files
│   └── generator.py     # Note processing engine
├── content/             # Your study notes
│   ├── mathematics/
│   ├── computer-science/
│   └── economics/
└── build/              # Generated static site
```

### Writing Mathematics

Use KaTeX syntax for mathematical expressions:

- Inline equations: `$E = mc^2$`
- Display equations:
```latex
$$
\frac{d}{dx}(x^n) = nx^{n-1}
$$
```

### Code Integration

Include code snippets with syntax highlighting:

````markdown
```python
def calculate_derivative(x, n):
    return n * (x ** (n-1))
```
````

## Development

### Local Development Server

Start the development server:

```bash
flask --app app run --debug
```

### Static Site Generation

Generate the static site:

```bash
flask --app app freeze
```

The static site will be generated in the `build` directory.

### Configuration

Customize the platform through `app/__init__.py`:

- `GITHUB_REPO`: Repository URL for source links
- `ENABLE_COMMENTS`: Toggle comment functionality
- `CONTENT_DIR`: Content directory location
- Additional Flask configuration options

## Deployment

The platform includes automated GitHub Pages deployment through GitHub Actions. The deployment workflow:

1. Triggers on pushes to the main branch
2. Sets up the Python environment
3. Installs dependencies
4. Generates the static site
5. Deploys to GitHub Pages

## Contributing

We welcome contributions! Follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This platform is built with:
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [KaTeX](https://katex.org/) - Mathematics rendering
- [Pygments](https://pygments.org/) - Syntax highlighting
- [Frozen-Flask](https://pythonhosted.org/Frozen-Flask/) - Static site generation