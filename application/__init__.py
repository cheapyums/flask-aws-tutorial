from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config.from_object('config')
db = SQLAlchemy(application)


'''
def isolation_level(level):
    """Return a Flask view decorator to set SQLAlchemy isolation level

    Usage::
        @main.route("/thingy/<id>", methods=["POST"])
        @isolation_level("SERIALIZABLE")
        def update_a_thing(id):
            ...
    """

    def decorator(view):
        def view_wrapper(*args, **kwargs):
            db.session.connection(execution_options={'isolation_level': level})
            return view(*args, **kwargs)

        return view_wrapper

    return decorator
    
#This may be useful for setting the SQLAlchemy engine
#db.engine.update_execution_options(isolation_level = "READ COMMITTED")
#print db.engine.get_execution_options()
'''