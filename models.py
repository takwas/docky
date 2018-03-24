from datetime import datetime
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def _generate_doc_uid():
    new_uid = uuid4().hex
    print 'Generating uid', new_uid
    return new_uid


ACTIVE_STATUS = 1
DISABLED_STATUS = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_updated = db.Column(db.DateTime, onupdate=datetime.now)
    status = db.Column(db.Integer, default=ACTIVE_STATUS)


class Doc(BaseModel):
    __tablename__ = 'docs'

    uid = db.Column(db.String(512), nullable=False, unique=True,
                    default=_generate_doc_uid)
    content = db.Column(db.Text)


class History(BaseModel):
    __tablename__ = 'histories'

    doc_id = db.Column(db.Integer, db.ForeignKey('docs.id'), nullable=False)
    content = db.Column(db.Text)


class User(BaseModel):

    username = db.Column(db.String(512), nullable=False, unique=True)
    password_hash = db.Column(db.String(512))
