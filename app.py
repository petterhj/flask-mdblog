# Imports
import configparser
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs, pygmented_markdown


# Config
config = configparser.ConfigParser()
config.read('flask-mdblog.ini')
config = config['app']

config = {
    'FLATPAGES_AUTO_RELOAD': config.getboolean('debug'),
    'FLATPAGES_ROOT': config.get('content_root'),
    'FLATPAGES_CONTENT_URL': config.get('content_url'),
    'FLATPAGES_MEDIA_URL': config.get('content_url') + config.get('media_url'),
    'FLATPAGES_EXTENSION': '.md',
    'FLATPAGES_MARKDOWN_EXTENSIONS': [
        'codehilite', 'fenced_code', 'footnotes', 
        'attr_list', 'tables'
    ],
}


# HTML renderer
def custom_renderer(body, fp_instance, page):
    body = body.replace('%CONTENT_URL%', config.get('FLATPAGES_CONTENT_URL'))
    body = body.replace('%MEDIA_URL%', config.get('FLATPAGES_MEDIA_URL'))
    return pygmented_markdown(body, flatpages=fp_instance)
config.update({'FLATPAGES_HTML_RENDERER': custom_renderer})


# App
app = Flask(__name__)
app.config.update(config)
pages = FlatPages(app)


# Route: Index
@app.route('/')
def index():
    posts = sorted(pages, reverse=True, key=lambda p: p.meta['published'])
    return render_template('index.html', pages=posts)


# Route: Page
@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)


# Route: Pygments style definition
@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('monokai'), 200, {'Content-Type': 'text/css'}