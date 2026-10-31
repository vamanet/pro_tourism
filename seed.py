from app import app
from extension import db          # must match your file name: extensions.py
from models import Place, User     # import BOTH

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(username="admin", role="admin")
    admin.set_password("1234")
    db.session.add(admin)

    db.session.add(Place(
        name="Eiffel Tower", city="Paris", category="landmark",
        description="Iron tower in Paris.", best_time="April to June",
        price="$30", image="eiffel.jpg", latitude=48.8584, longitude=2.2945))

    db.session.commit()
    print("Database ready!")