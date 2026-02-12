from flask import jsonify,request, render_template, redirect, url_for, session, flash
from datetime import datetime
from main import app
from models import db, Host,Event,User,EventParticipation
from werkzeug.utils import secure_filename
from functools import wraps
import os

print("ROUTES.PY LOADED")
print("ROUTES.PY END")

@app.route("/hosts")
def show_hosts():
    hosts = Host.query.all()   # READ from DB
    return render_template("hosts.html", hosts=hosts)

@app.route("/add-host", methods=["GET", "POST"])
def add_host():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        host = Host(name=name, email=email, password=password)
        db.session.add(host)
        db.session.commit()

        return redirect(url_for("show_hosts"))

    return render_template("add_host.html")

@app.route("/edit-host/<int:id>", methods=["GET", "POST"])
def edit_host(id):
    host = Host.query.get_or_404(id)

    if request.method == "POST":
        host.name = request.form["name"]
        host.email = request.form["email"]
        host.password = request.form["password"]

        db.session.commit()
        return redirect(url_for("show_hosts"))

    return render_template("edit_host.html", host=host)

@app.route("/delete-host/<int:id>")
def delete_host(id):
    host = Host.query.get_or_404(id)
    db.session.delete(host)
    db.session.commit()
    return redirect(url_for("show_hosts"))


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/hackathon")
def hackathon():
    return render_template("hackathon.html")




@app.route("/bootcamp")
def bootcamp():
    return render_template("bootcamp.html")

@app.route("/meetup")
def meetup():
    return render_template("meetup.html")




@app.route("/contact")
def contact():
    return render_template("contact-preferences.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            user.last_login = datetime.utcnow()
            db.session.commit()

            session["user_id"] = user.id
            session["role"] = "user"
            session["name"] = user.full_name

            flash("Login successful!", "success")
            return redirect("/")

        host = Host.query.filter_by(email=email).first()
        if host and host.check_password(password):
            host.last_login = datetime.utcnow()
            db.session.commit()

            session["host_id"] = host.id
            session["role"] = "host"
            session["name"] = host.full_name

            flash("Login successful!", "success")
            return redirect("/")


        flash("Invalid email or password", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/dashboard")
def user_dashboard():
    return "User Dashboard (login successful)"


@app.route("/host/dashboard")
def host_dashboard():
    return "Host Dashboard (login successful)"


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("login"))


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        # Common fields
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        is_host = request.form.get("is_host")


        if User.query.filter_by(email=email).first() or Host.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
            return redirect(url_for("signup"))


        if is_host:

            logo_filename = None
            logo_file = request.files.get("company_logo")

            if logo_file and allowed_file(logo_file.filename):
                filename = secure_filename(logo_file.filename)
                logo_filename = f"{int(datetime.utcnow().timestamp())}_{filename}"
                logo_path = os.path.join(app.config["UPLOAD_FOLDER"], logo_filename)
                logo_file.save(logo_path)

            host = Host(
                full_name=full_name,
                email=email,
                company_name=request.form.get("company_name"),
                company_logo=logo_filename,
                website=request.form.get("website"),
                city=request.form.get("city"),
                state=request.form.get("state"),
                created_at=datetime.utcnow(),
                last_login=None
            )

            host.set_password(password)

            db.session.add(host)
            db.session.commit()

            flash("Host account created successfully. Please login.", "success")
            return redirect(url_for("login"))

        skills_list = request.form.getlist("skills")
        skills_str = ",".join(skills_list)

        user = User(
            full_name=full_name,
            email=email,
            description=request.form.get("description"),
            college=request.form.get("college"),
            course=request.form.get("course"),
            year=request.form.get("year"),
            skills=skills_str,
            created_at=datetime.utcnow(),
            last_login=None
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")





@app.route("/api/hackathons", methods=["GET"])
def get_hackathons():
    search = request.args.get("search")
    status = request.args.get("status")
    city = request.args.get("city")
    skill = request.args.get("skill")
    skill_level = request.args.get("skill_level")

    query = Event.query.filter(Event.type_of_event == "hackathon")

    if search:
        query = query.filter(Event.title.ilike(f"%{search}%"))

    if status:
        query = query.filter(Event.status == status)

    if city:
        query = query.filter(
            (Event.city == city) | (Event.location == city)
        )

    if skill_level:
        query = query.filter(Event.skill_level == skill_level)

    hackathons = query.order_by(Event.created_at.desc()).all()

    # Skill (CSV match)
    if skill:
        hackathons = [
            h for h in hackathons
            if skill.lower() in [s.strip().lower() for s in h.skills.split(",")]
        ]

    return jsonify([
        {
            "id": h.id,
            "title": h.title,
            "description": h.description,
            "start_date": h.start_date.isoformat(),
            "end_date": h.end_date.isoformat(),
            "location": h.location,
            "city": h.city,
            "state": h.state,
            "mode": h.mode,
            "status": h.status,
            "skills": h.skills,
            "skill_level": h.skill_level,
            "max_participants": h.max_participants,
            "banner_image": h.banner_image
        }
        for h in hackathons
    ])



@app.route("/api/hackathons/latest")
def latest_hackathons():
    hackathons = (
        Event.query
        .filter(Event.type_of_event == "hackathon")
        .order_by(Event.created_at.desc())
        .limit(3)
        .all()
    )

    return jsonify([
        {
            "id": h.id,
            "title": h.title,
            "description": h.description,

            "start_date": h.start_date.isoformat(),
            "end_date": h.end_date.isoformat(),

            "mode": h.mode,
            "city": h.city,
            "location": h.location,

            # 💰 IMPORTANT
            "registration_fee": h.registration_fee,

            # optional UI info
            "skill_level": h.skill_level,
            "banner_image": h.banner_image,

            "attending": h.attending
        }
        for h in hackathons
    ])

@app.route("/api/workshops/latest")
def latest_workshops():
    workshops = (
        Event.query
        .filter(Event.type_of_event == "workshop")
        .order_by(Event.created_at.desc())
        .limit(3)
        .all()
    )

    return jsonify([
        {
            "id": w.id,
            "title": w.title,
            "description": w.description,

            "start_time": w.start_time.isoformat() if w.start_time else None,
            "end_time": w.end_time.isoformat() if w.end_time else None,

            "registration_fee": w.registration_fee,

            "skill_level": w.skill_level,
            "host_name": w.host.company_name if w.host else "TechHub",

            "attending": w.attending,
        }
        for w in workshops
    ])



@app.route("/api/meetups/latest")
def latest_meetups():
    meetups = (
        Event.query
        .filter(Event.type_of_event == "meetup")
        .order_by(Event.created_at.desc())
        .limit(2)   # 2 or 4 depending on your layout
        .all()
    )

    return jsonify([
        {
            "id": m.id,
            "title": m.title,
            "description": m.description,

            "start_date": m.start_date.isoformat(),
            "start_time": m.start_time.isoformat() if m.start_time else None,
            "end_time": m.end_time.isoformat() if m.end_time else None,

            "mode": m.mode,
            "city": m.city,
            "location": m.location,

            "attending": m.attending
        }
        for m in meetups
    ])




def host_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "host":
            flash("Host access required", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/host-event")
@host_required
def host_event():
    return render_template("host-event.html")




@app.route("/host-event", methods=["POST"])
@host_required
def create_event():
    host_id = session.get("host_id")


    def parse_date(value):
        return datetime.strptime(value, "%Y-%m-%d").date() if value else None

    title = request.form.get("title")
    description = request.form.get("description")
    event_type = request.form.get("event_type")
    start_raw = request.form.get("start_datetime")
    end_raw = request.form.get("end_datetime")
    mode = request.form.get("format")

    if not all([title, description, event_type, start_raw, end_raw, mode]):
        flash("Please fill all required fields (including event format)", "danger")
        return redirect(url_for("host_event"))


    start_dt = datetime.fromisoformat(start_raw)
    end_dt = datetime.fromisoformat(end_raw)


    skills_list = request.form.getlist("skills")
    skills = ", ".join(skills_list)


    registration_fee = int(request.form.get("registration_fee", 0))

    first_prize = request.form.get("first_prize")
    second_prize = request.form.get("second_prize")
    third_prize = request.form.get("third_prize")
    other_rewards = request.form.get("other_rewards")


    platform = request.form.get("platform")

    submission_start_date = parse_date(request.form.get("submission_start_date"))
    submission_end_date = parse_date(request.form.get("submission_end_date"))
    judging_start_date = parse_date(request.form.get("judging_start_date"))
    judging_end_date = parse_date(request.form.get("judging_end_date"))
    winner_announcement_date = parse_date(request.form.get("winner_announcement_date"))


    location = request.form.get("location")
    city = request.form.get("city")
    state = request.form.get("state")

    if mode == "online":
        location = "Online"
        city = None
        state = None

    host = Host.query.get(host_id)

    if not host:
        flash("Host not found", "danger")
        return redirect(url_for("host_event"))


    event = Event(
        title=title,
        description=description,
        type_of_event=event_type,

        start_date=start_dt.date(),
        end_date=end_dt.date(),
        start_time=start_dt.time(),
        end_time=end_dt.time(),

        submission_start_date=submission_start_date,
        submission_end_date=submission_end_date,
        judging_start_date=judging_start_date,
        judging_end_date=judging_end_date,
        winner_announcement_date=winner_announcement_date,

        mode=mode,
        platform=platform,
        location=location,
        city=city,
        state=state,

        status="upcoming",

        skills=skills,
        skill_level=request.form.get("skill_level", "any"),

        max_participants=(
            int(request.form.get("max_participants"))
            if request.form.get("max_participants")
            else None
        ),

        registration_fee=registration_fee,
        first_prize=int(first_prize) if first_prize else None,
        second_prize=int(second_prize) if second_prize else None,
        third_prize=int(third_prize) if third_prize else None,
        other_rewards=other_rewards,

        host_id=host_id,
        banner_image=host.company_logo,
    )

    db.session.add(event)
    db.session.commit()

    flash("Event created successfully!", "success")
    return redirect(url_for("host_event"))


@app.route("/workshop")
def workshop():
    return render_template("workshop.html")


@app.route("/api/workshops", methods=["GET"])
def get_workshops():
    search = request.args.get("search")
    status = request.args.get("status")
    city = request.args.get("city")
    skill = request.args.get("skill")
    skill_level = request.args.get("skill_level")

    query = Event.query.filter(Event.type_of_event == "workshop")

    if search:
        query = query.filter(Event.title.ilike(f"%{search}%"))

    if status:
        query = query.filter(Event.status == status)

    if city:
        query = query.filter(
            (Event.city == city) | (Event.location == city)
        )

    if skill_level:
        query = query.filter(Event.skill_level == skill_level)

    workshops = query.order_by(Event.created_at.desc()).all()

    if skill:
        workshops = [
            w for w in workshops
            if skill.lower() in [s.strip().lower() for s in w.skills.split(",")]
        ]

    return jsonify([
        {
            "id": w.id,
            "title": w.title,
            "description": w.description,
            "start_date": w.start_date.isoformat(),
            "end_date": w.end_date.isoformat(),
            "start_time": w.start_time.isoformat() if w.start_time else None,
            "end_time": w.end_time.isoformat() if w.end_time else None,
            "location": w.location,
            "city": w.city,
            "state": w.state,
            "mode": w.mode,
            "status": w.status,
            "skills": w.skills,
            "skill_level": w.skill_level,
            "max_participants": w.max_participants,
            "banner_image": w.banner_image
        }
        for w in workshops
    ])

@app.route("/api/meetups", methods=["GET"])
def get_meetups():
    search = request.args.get("search")
    city = request.args.get("city")
    topic = request.args.get("topic")

    query = Event.query.filter(Event.type_of_event == "meetup")

    if search:
        query = query.filter(Event.title.ilike(f"%{search}%"))

    if city:
        query = query.filter(
            (Event.city == city) | (Event.location == city)
        )

    meetups = query.order_by(Event.created_at.desc()).all()

    # topic filter (skills-based)
    if topic:
        meetups = [
            m for m in meetups
            if m.skills and topic.lower() in
            [s.strip().lower() for s in m.skills.split(",")]
        ]

    return jsonify([
        {
            "id": m.id,
            "title": m.title,
            "description": m.description,

            "start_date": m.start_date.isoformat(),
            "start_time": m.start_time.isoformat() if m.start_time else None,
            "end_time": m.end_time.isoformat() if m.end_time else None,

            "mode": m.mode,
            "city": m.city,
            "location": m.location,

            "skills": m.skills,
            "attending": m.attending
        }
        for m in meetups
    ])


@app.route("/api/bootcamps", methods=["GET"])
def get_bootcamps():
    bootcamps = (
        Event.query
        .filter(Event.type_of_event == "bootcamp")
        .order_by(Event.created_at.desc())
        .all()
    )

    result = []

    for b in bootcamps:
        duration_days = None
        if b.start_date and b.end_date:
            duration_days = (b.end_date - b.start_date).days

        result.append({
            "id": b.id,
            "title": b.title,
            "description": b.description,

            "registration_fee": b.registration_fee or 0,

            "duration_days": duration_days,

            "skills": b.skills or "",

            "instructor": (
                b.host.company_name
                if hasattr(b, "host") and b.host
                else "TechHub"
            )
        })

    return jsonify(result)

@app.route("/api/bootcamps/latest")
def latest_bootcamps():
    bootcamps = (
        Event.query
        .filter(Event.type_of_event == "bootcamp")
        .order_by(Event.created_at.desc())
        .limit(3)
        .all()
    )

    result = []

    for b in bootcamps:
        duration_days = None
        if b.start_date and b.end_date:
            duration_days = (b.end_date - b.start_date).days

        result.append({
            "id": b.id,
            "title": b.title,
            "description": b.description,

            "registration_fee": b.registration_fee or 0,

            "duration_days": duration_days,

            "instructor": (
                b.host.company_name
                if hasattr(b, "host") and b.host
                else "TechHub"
            )
        })

    return jsonify(result)



@app.route("/event/<event_type>/<int:event_id>")
def event_detail(event_type, event_id):
    event = Event.query.filter_by(
        id=event_id,
        type_of_event=event_type
    ).first_or_404()

    rendering_template=""
    if event_type=="hackathon":
        rendering_template = "hackathon_details.html"
    elif event_type=="meetup":
        rendering_template = "meetup_details.html"
    elif event_type=="workshop":
        rendering_template = "workshop_details.html"
    elif event_type=="bootcamp":
        rendering_template = "bootcamp_details.html"

    already_registered = False
    user_id = session.get("user_id")
    if user_id:
        for p in event.participants:
            if p.user_id == user_id:
                already_registered = True
                break


    return render_template(
        rendering_template,
        event=event,
        already_registered=already_registered
    )

@app.route("/profile")
def profile():
    role = session.get("role")
    user_id = session.get("user_id")
    host_id = session.get("host_id")

    if not role:
        flash("Please login first", "warning")
        return redirect(url_for("login"))


    if role == "user":
        user = User.query.get_or_404(user_id)

        participations = EventParticipation.query.filter_by(
            user_id=user_id
        ).all()

        list_hackathon = []
        list_bootcamp = []
        list_meetup = []
        list_workshop = []

        for p in participations:
            event = Event.query.get(p.event_id)
            if not event:
                continue

            if p.event_type == "hackathon":
                list_hackathon.append(event)
            elif p.event_type == "bootcamp":
                list_bootcamp.append(event)
            elif p.event_type == "meetup":
                list_meetup.append(event)
            elif p.event_type == "workshop":
                list_workshop.append(event)

        return render_template(
            "profile.html",
            user=user,

            list_hackathon=list_hackathon,
            list_bootcamp=list_bootcamp,
            list_meetup=list_meetup,
            list_workshop=list_workshop,

            hackathon_attended=len(list_hackathon),
            bootcamp_attended=len(list_bootcamp),
            meetup_attended=len(list_meetup),
            workshop_attended=len(list_workshop),
        )


    elif role == "host":
        host = Host.query.get_or_404(host_id)

        events = Event.query.filter_by(
            host_id=host_id
        ).all()

        list_hackathon = []
        list_bootcamp = []
        list_meetup = []
        list_workshop = []

        for event in events:
            if event.type_of_event == "hackathon":
                list_hackathon.append(event)
            elif event.type_of_event == "bootcamp":
                list_bootcamp.append(event)
            elif event.type_of_event == "meetup":
                list_meetup.append(event)
            elif event.type_of_event == "workshop":
                list_workshop.append(event)

        total_events_created = (
            len(list_hackathon)
            + len(list_bootcamp)
            + len(list_meetup)
            + len(list_workshop)
        )

        return render_template(
            "profile_host.html",
            host=host,

            list_hackathon=list_hackathon,
            list_bootcamp=list_bootcamp,
            list_meetup=list_meetup,
            list_workshop=list_workshop,

            hackathon_created=len(list_hackathon),
            bootcamp_created=len(list_bootcamp),
            meetup_created=len(list_meetup),
            workshop_created=len(list_workshop),
            total_events_created=total_events_created
        )



@app.route("/event/<int:event_id>/participate", methods=["POST"])
def participate_event(event_id):


    user_id = session.get("user_id")
    role = session.get("role")

    if not user_id:
        flash("Please login to participate", "warning")
        return redirect(url_for("login"))

    if role != "user":
        flash("Only users can participate in events", "danger")
        return redirect(request.referrer)


    event = Event.query.get_or_404(event_id)


    existing = EventParticipation.query.filter_by(
        user_id=user_id,
        event_id=event.id
    ).first()

    if existing:
        flash("You are already registered for this event", "info")
        return redirect(request.referrer)

    if event.max_participants:
        if event.attending is None:
            event.attending = 0

        if event.attending >= event.max_participants:
            flash("Event is full", "danger")
            return redirect(request.referrer)


    participation = EventParticipation(
        user_id=user_id,
        event_id=event.id,
        event_type=event.type_of_event
    )

    db.session.add(participation)


    event.attending = (event.attending or 0) + 1

    db.session.commit()

    flash("Successfully registered 🎉", "success")
    return redirect(request.referrer)

@app.route("/host/event/<int:event_id>")
@host_required
def host_event_detail(event_id):
    host_id = session.get("host_id")


    event = Event.query.filter_by(
        id=event_id,
        host_id=host_id
    ).first_or_404()


    participations = EventParticipation.query.filter_by(
        event_id=event.id
    ).all()


    participants = []

    for p in participations:
        user = User.query.get(p.user_id)
        if user:
            participants.append(user)

    return render_template(
        "host_event_detail.html",
        event=event,
        participants=participants
    )
