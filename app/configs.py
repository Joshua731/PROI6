from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:capua123@localhost:1433/dashua'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '10b15r19_JOSHUA'

jwt = JWTManager(app)
db = SQLAlchemy(app)
