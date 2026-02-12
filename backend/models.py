from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)


    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type_of_event = db.Column(db.String(20), nullable=False)  # hackathon/workshop/meetup/bootcamp


    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    submission_start_date = db.Column(db.Date)
    submission_end_date = db.Column(db.Date)


    judging_start_date = db.Column(db.Date)
    judging_end_date = db.Column(db.Date)


    winner_announcement_date = db.Column(db.Date)


    mode = db.Column(db.String(20))  # online/offline/hybrid
    platform = db.Column(db.String(100))  # zoom, meet, etc.

    location = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))


    max_participants = db.Column(db.Integer)
    attending = db.Column(db.Integer, default=0)


    skills = db.Column(db.Text)
    skill_level = db.Column(db.String(20), default="any")


    registration_fee = db.Column(db.Integer, default=0)

    first_prize = db.Column(db.String(100))
    second_prize = db.Column(db.String(100))
    third_prize = db.Column(db.String(100))
    other_rewards = db.Column(db.Text)


    status = db.Column(db.String(20), default="upcoming")
    banner_image = db.Column(db.String(255))

    host_id = db.Column(db.Integer, db.ForeignKey("hosts.id"), nullable=False)
    host = db.relationship("Host", backref="events")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Event {self.title} ({self.type_of_event})>"


class Host(db.Model):
    __tablename__ = "hosts"

    id = db.Column(db.Integer, primary_key=True)

    # Uses full_name from signup (NO duplicate admin name)
    full_name = db.Column(db.String(120), nullable=False)

    company_name = db.Column(db.String(150), nullable=False)
    company_logo = db.Column(db.String(255))

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    website = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))

    events_created = db.Column(db.Integer, default=0)
    company_rating = db.Column(db.Float, default=0.0)

    role = db.Column(db.String(20), default="host")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<Host {self.company_name}>"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text)
    college = db.Column(db.String(150))
    course = db.Column(db.String(100))
    year = db.Column(db.String(50))

    skills = db.Column(db.Text)

    role = db.Column(db.String(20), default="user")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.email}>"

class EventParticipation(db.Model):
    __tablename__ = "event_participations"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id"),
        nullable=False
    )

    event_type = db.Column(db.String(20), nullable=False)

    status = db.Column(db.String(20), default="registered")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships (ONLY HERE)
    user = db.relationship("User", backref="participations")
    event = db.relationship("Event", backref="participants")

    __table_args__ = (
        db.UniqueConstraint("user_id", "event_id", name="uq_user_event"),
    )

    def __repr__(self):
        return f"<EventParticipation user={self.user_id} event={self.event_id}>"
