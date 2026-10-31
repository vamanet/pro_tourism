from extension import db

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50))
    category = db.Column(db.String(30))
    description = db.Column(db.Text)
    best_time = db.Column(db.String(100))
    price = db.Column(db.String(50))
    image = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)