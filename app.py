from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet, AddPetForm, EditPetForm
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField
from wtforms.validators import Length, URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'password'  

connect_db(app)
db.create_all()


@app.route('/', methods=["GET"])
def homepage():
    pets = Pet.query.all()
    return render_template("pets.html", pets=pets)

# @app.route('/<int:pet_id>', methods=["GET"])
# def view_pet(pet_id):
#     pet = Pet.query.get_or_404(pet_id)
#     return render_template("pet_view.html", pet=pet)

@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """Pet add form; handle adding."""

    form = AddPetForm()

    if form.validate_on_submit():
        pet = Pet(name=form.name.data, species=form.species.data, photo_url=form.photo_url.data, age=form.age.data, notes=form.notes.data)
        db.session.add(pet)
        db.session.commit()
        flash(f"Added {pet.name}")
        return redirect("/add")

    else:
        return render_template(
            "pet_add_form.html", form=form)

@app.route('/<int:pet_id>', methods=["GET", "POST"])
def edit_pet(pet_id):
    """Pet edit form; handle editing pet"""

    form = EditPetForm()

    if form.validate_on_submit():
        pet = Pet.query.get_or_404(pet_id)
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.add(pet)
        db.session.commit()
        flash(f"Updated {pet.name}")
        return redirect (f"/{pet.id}")

    else:
        pet = Pet.query.get_or_404(pet_id)
        return render_template("pet_view.html", form=form, pet=pet)

@app.route('/<int:pet_id>/delete', methods=["POST"])
def pet_delete(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    pets = Pet.query.all()
    return redirect('/', code=302)
