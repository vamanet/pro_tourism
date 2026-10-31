import os
from flask import Flask
from setting.config import Config
from extension import db
from routes import main,admin,auth



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)