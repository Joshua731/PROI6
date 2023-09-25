from app import app

from app.templates.index import index
from app.templates.interface import interface
from app.templates.lista import lista



@app.route('/')
@app.route('/index')
def indice():
    return index.index()


@app.route('/interface')
def interfaces():
    return interface.index()

@app.route('/lista')
def listas():
    return lista.index()
