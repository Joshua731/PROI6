from app import app

from app.templates.index import index
from app.templates.interface import interface
from app.templates.dashboard import dashboard


@app.route('/')
@app.route('/index')
def indice():
    return index.index()


@app.route('/interface')
def interfaces():
    return interface.index()

@app.route('/dashboard')
def interfaces():
    return dashboard.index()
