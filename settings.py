from flask import Flask

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\alexandrupopescu\\Documents\\Repositories\\__Other Repositories\\python-flask-rest-api\\database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False