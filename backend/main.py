from flask import Flask
from models import db
import os

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///TechEvent.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = "techhub-secret-key-change-this"


UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads", "company_logos")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


db.init_app(app)

from models import User, Host, Event


with app.app_context():
    db.create_all()


from routes import *


if __name__ == "__main__":
    app.run(debug=True)
