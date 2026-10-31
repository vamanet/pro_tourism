import os
import uuid
from flask import (Blueprint, render_template, request, redirect,
                   url_for, flash, current_app)
from extension import db
from models import Place
from setting.decorators import admin_required

admin = Blueprint("admin", __name__, url_prefix="/admin")

ALLOWED = {"png", "jpg", "jpeg", "webp"}


def save_image(file):
    """Save an uploaded image and return the new filename (or None)."""
    if not file or file.filename == "":
        return None
    if "." not in file.filename:
        return None
    ext = file.filename.rsplit(".", 1)[1].lower()
    if ext not in ALLOWED:
        return None
    filename = f"{uuid.uuid4().hex}.{ext}"        # unique name, no clashes
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    return filename


def delete_image(filename):
    if filename:
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        if os.path.exists(path):
            os.remove(path)


def fill_place(place):
    """Copy form fields into the Place object. Returns False if invalid."""
    try:
        place.latitude = float(request.form["latitude"])
        place.longitude = float(request.form["longitude"])
    except ValueError:
        flash("Latitude and longitude must be numbers")
        return False

    place.name = request.form["name"].strip()
    place.city = request.form["city"].strip()
    place.category = request.form["category"].strip().lower()
    place.description = request.form["description"].strip()
    place.best_time = request.form["best_time"].strip()
    place.price = request.form["price"].strip()

    if not place.name:
        flash("Name is required")
        return False
    return True


@admin.route("/")
@admin_required
def places():
    return render_template("admin/places.html", places=Place.query.order_by(Place.id.desc()).all())


@admin.route("/places/new", methods=["GET", "POST"])
@admin_required
def add_place():
    if request.method == "POST":
        place = Place()
        if fill_place(place):
            place.image = save_image(request.files.get("image"))
            db.session.add(place)
            db.session.commit()
            flash("Place added")
            return redirect(url_for("admin.places"))
    return render_template("admin/place_form.html", place=None)


@admin.route("/places/<int:place_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_place(place_id):
    place = db.get_or_404(Place, place_id)
    if request.method == "POST":
        if fill_place(place):
            new_image = save_image(request.files.get("image"))
            if new_image:                       # a new photo was uploaded
                delete_image(place.image)       # remove the old file
                place.image = new_image
            db.session.commit()
            flash("Place updated")
            return redirect(url_for("admin.places"))
    return render_template("admin/place_form.html", place=place)


@admin.route("/places/<int:place_id>/delete", methods=["POST"])
@admin_required
def delete_place(place_id):
    place = db.get_or_404(Place, place_id)
    delete_image(place.image)
    db.session.delete(place)
    db.session.commit()
    flash("Place deleted")
    return redirect(url_for("admin.places"))