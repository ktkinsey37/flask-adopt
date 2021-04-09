from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import Length, URL, Optional, NumberRange

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Pet(db.Model):
    def __repr__(self):
        p = self
        return f'<Pet {p.id} {p.name} {p.species} {p.age} {p.available}>'

    __tablename__ = 'pets'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    name = db.Column(db.String(50),
                    nullable=False)

    species = db.Column(db.String(50), nullable=False)

    photo_url = db.Column(db.String)

    age = db.Column(db.Integer)

    notes = db.Column(db.String)

    available = db.Column(db.Boolean, nullable=False, default=True)



class AddPetForm(FlaskForm):
    """Form for adding pets."""

    name = StringField("Pet Name")
    species = SelectField('Species',
  choices=[('Cat', 'Cat'), ('Dog', 'Dog'), ('Porcupine', 'Porcupine')]
)
    photo_url = URLField("URL to Pet's Picture",
                        validators=[URL(), Optional()])
    age = IntegerField("Pet's Age in Years",
                        validators=[NumberRange(0,30)])
    notes = StringField("Any Addition Notes for Pet")

class EditPetForm(FlaskForm):
    """Form for editing pets."""

    photo_url = URLField("URL to Pet's Picture",
                        validators=[URL(), Optional()])
    notes = StringField("Any Additional Notes for Pet")
    available = BooleanField("Is this pet still available for adoption?")