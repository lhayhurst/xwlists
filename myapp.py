import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

#see https://www.pythonanywhere.com/wiki/WebAppClientIPAddresses
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql.elements import _clause_element_as_expr


def remote_address(request):
    if request.headers.has_key( 'X-Real-IP'):
        return request.headers[ 'X-Real-IP' ]
    else:
        return request.remote_addr

#rollup help
#see https://groups.google.com/forum/#!msg/sqlalchemy/Pj5T8hO_ibQ/LrmBcIBxnNwJ
class rollup(ColumnElement):
    def __init__(self, *elements):
        self.elements = [_clause_element_as_expr(e) for e in elements]

@compiles(rollup, "mysql")
def _mysql_rollup(element, compiler, **kw):
    return "%s WITH ROLLUP" % (', '.join([compiler.process(e, **kw) for e in element.elements]))


class MyDatabaseConnector(object):
    engine = None
    Session = None
    connection = None
    base = None

    def __init__(self):
        self.connect()

    def connect(self):
        if self.engine is None:
            self.engine = create_engine(os.getenv('LOCAL_DB_URL'), echo=False, pool_size=100, pool_recycle=299,
                                        pool_timeout=20)

            if self.Session is None:
                self.Session = scoped_session(sessionmaker(bind=self.engine, expire_on_commit=False))
                self.Session.configure( bind=self.engine)

            if self.connection is None:
                self.connection = self.engine.connect()

            if self.base is None:
                self.base = declarative_base()

    def get_base(self):
        self.connect()
        return self.base

    def get_session(self):
        self.connect()
        return self.Session

    def get_engine(self):
        self.connect()
        return self.engine

    def close(self):
        self.Session.remove()


db_connector   = MyDatabaseConnector()
challonge_user = os.getenv('CHALLONGE_USER')
challonge_key  = os.getenv('CHALLONGE_API_KEY')


def create_app():
    app = Flask(__name__ , static_folder='static')
    app.secret_key = 'q}q?fpX+QgwwKd8u7k3wsJgmY2tRu)'
    return app