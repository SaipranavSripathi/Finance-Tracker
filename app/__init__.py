import os
from flask import Flask
from app.extensions import db, migrate
from flask_sqlalchemy import SQLAlchemy
from app.init_db import execute_sql_file
from app.routes import api

def create_app():
    app = Flask(__name__,static_folder=os.path.join(os.getcwd(), 'static'), template_folder=os.path.join(os.getcwd(), 'templates'))
    app.config.from_object('app.config.Config')

    db.init_app(app)


    # Run DDL SQL file
    ddl_file_path = '/Users/spartan/Documents/GitHub/DBMS-Final-Project/projectEnv/app/database_ddl.sql' #'projectEnv/app/database_ddl.sql'
    execute_sql_file(app, ddl_file_path)
    #execute_triggers(app)
    migrate.init_app(app, db)

    from app.routes import api
    app.register_blueprint(api)
    # with app.app_context():
    #     from app import routes
    return app

