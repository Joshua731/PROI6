from app import app

from app.templates.index import index
from app.templates.interface import interface



@app.route('/')
@app.route('/index')
def indice():
    return index.index()


@app.route('/interface')
def interfaces():
    return interface.index()


