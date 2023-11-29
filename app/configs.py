from app import app
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '10b15r19_JOSHUA'
db = SQLAlchemy(app)

usuario = 'capua'
senha = 'Capua123#'
base = 'bancobrasil'
ip = '201.48.100.251'
porta = 1434
