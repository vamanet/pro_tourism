from flask import Blueprint, render_template, request
from extension import db
from models import Place
from flask import redirect, url_for

from setting.decorators import login_required

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return redirect(url_for("main.dashboard"))

@main.route("/dashboard")
@login_required
def dashboard():
    places = Place.query.order_by(Place.id.desc()).limit(6).all()
    return render_template("dashboard.html", places=places)

@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@main.route("/settings")
@login_required
def settings():
    return render_template("setting.html")

@main.route("/places")
def places():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "")

    query = Place.query
    if q:
        query = query.filter(Place.name.ilike(f"%{q}%") | Place.city.ilike(f"%{q}%"))
    if category:
        query = query.filter_by(category=category)

    categories = [c[0] for c in db.session.query(Place.category).distinct()]
    return render_template("places.html", places=query.all(),
                           categories=categories, q=q, selected=category)

@main.route("/place/<int:place_id>")
def place_detail(place_id):
    place = db.get_or_404(Place, place_id)
    return render_template("place_detail.html", place=place)

@main.route("/map")
def map_page():
    data = [{"id": p.id, "name": p.name, "city": p.city,
             "lat": p.latitude, "lng": p.longitude}
            for p in Place.query.all()]
    return render_template("map.html", places=data)