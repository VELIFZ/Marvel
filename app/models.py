from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import INTEGER

db = SQLAlchemy()

from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from uuid import uuid4 

from flask_login import LoginManager, UserMixin 
login = LoginManager()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin): 
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True) 
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    char = db.relationship('Marvel', backref='char')

    def __init__(self,username, email, password): 
        self.username= username
        self.email = email.lower()
        self.password = generate_password_hash(password)
        self.id = str(uuid4())

class Marvel(db.Model):
    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id')) 
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    comics_appeared_in = db.Column(db.Integer(), nullable=False)
    super_power = db.Column(db.String(200), nullable=False)
    date_c = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __init__(self, dict):
        self.id = str(uuid4())
        self.user_id = dict.get('user_id')
        self.name = dict['name'].name()
        self.description = dict['description']
        self.comics_appeared_in = dict['comics_appeared_in']
        self.super_power = dict['super_power']
        self.date_c = dict.get('date_c')
        
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'comics_appeared_in': self.comics_appeared_in,
            'date_c': self.date_c,
            'super_power': self.super_power
        }

    def from_dict(self, dict):
        if dict.get('name'):
            self.name = dict['name'].name()
        if dict.get('description'):
            self.description = dict['description']
        if dict.get('comics_appeared_in'):
            self.comics_appeared_in = dict['comics_appeared_in']
        if dict.get('date_posted'):
            self.date_posted = dict['date_posted']
        if dict.get('super_power'):
            self.super_power = dict['super_power']