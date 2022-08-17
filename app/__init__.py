from flask import Flask
from .extensions import db
from .views import view



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://user1:abcd1234@localhost/mydb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.init_app(app)
    db.create_all(app=app)

    app.register_blueprint(view)

    return app

