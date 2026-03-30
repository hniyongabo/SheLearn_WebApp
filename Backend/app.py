from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory, jsonify
from datetime import timedelta, datetime
from dotenv import load_dotenv
import os, json

load_dotenv()   # loads Backend/.env into os.environ before anything else

app = Flask(__name__, template_folder='templates', static_folder='static')
_secret = os.environ.get('SECRET_KEY')
if not _secret:
    raise RuntimeError("SECRET_KEY environment variable is not set. Add it to your .env file.")
app.secret_key = _secret
app.permanent_session_lifetime = timedelta(days=2)

# ── Database ──────────────────────────────────────────────────────────────────
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shelearn.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from db import db, User, Progress, LessonContent
db.init_app(app)

with app.app_context():
    db.create_all()

# ── Static file routes ───────────────────────────────────────────────────────
@app.route('/styles.css')
def styles():
    return send_from_directory('static', 'styles.css')

@app.route('/landing-sections.css')
def landing_sections_css():
    return send_from_directory('static', 'landing-sections.css')

@app.route('/script.js')
def script_js():
    return send_from_directory('static', 'script.js')

@app.route('/hero-bg.jpeg')
def hero_bg():
    return send_from_directory('static', 'hero-bg.jpeg')


@app.route('/ladder.jpeg')
def ladder_jpeg():
    return send_from_directory('static', 'ladder.jpeg')

@app.route('/dev.jpeg')
def dev_jpeg():
    return send_from_directory('static', 'dev.jpeg')

@app.route('/data_sc.jpeg')
def data_sc_jpeg():
    return send_from_directory('static', 'data_sc.jpeg')

# ── Auth ──────────────────────────────────────────────────────────────────────
@app.route('/logout')
def logout():
    name = session.get('name', '')
    session.clear()
    flash(f"Goodbye, {name}! You have been logged out.", "info")
    return redirect(url_for('login'))

# ── Page routes ───────────────────────────────────────────────────────────────
@app.route('/')
@app.route('/landing')
def landing():
    return render_template('landing.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "error")
            return redirect(url_for('login'))

        session.permanent    = True
        session["user_id"]   = user.id
        session["name"]      = user.name
        session["email"]     = user.email
        session["user_role"] = user.role
        session["track"]     = user.track or ""
        session["is_new"]    = False  # existing account logging back in

        flash(f"Welcome back, {user.name}!", "success")

        if user.role == "admin":
            return redirect(url_for('admin'))
        if user.role == "facilitator":
            return redirect(url_for('facilitator'))
        if user.track == "software-development":
            return redirect(url_for('dev_student'))
        return redirect(url_for('student', name=user.name))

    return render_template("login.html")


@app.route("/SignUp", methods=['GET', 'POST'])
def SignUp():
    if request.method == 'POST':
        name     = request.form.get("name", "").strip()
        track    = request.form.get("track", "").strip()
        email    = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if name == "":
            flash("Please enter your full name.", "error")
            return redirect(url_for('SignUp'))
        if track == "":
            flash("Please select a course before signing up.", "error")
            return redirect(url_for('SignUp'))
        if not email:
            flash("Please enter your email address.", "error")
            return redirect(url_for('SignUp'))

        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists. Please log in.", "error")
            return redirect(url_for('login'))

        new_user = User(name=name, email=email, role='student', track=track)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        # No Progress records are created here — every new student starts with
        # zero completed lessons. Progress is only added when they click
        # "Mark as Complete" on a lesson page (POST /api/user/progress).

        session.permanent    = True
        session["user_id"]   = new_user.id
        session["name"]      = name
        session["email"]     = email
        session["user_role"] = "student"
        session["track"]     = track
        session["is_new"]    = True   # brand-new signup

        flash(f"Welcome, {name}! Your account has been created successfully.", "success")

        if track == "software-development":
            return redirect(url_for('dev_student'))
        return redirect(url_for('student', name=name))

    return render_template("SignUp.html")


@app.route("/dashboard")
def dashboard():
    name = session.get("name", "")
    if session.get("track") == "software-development":
        return redirect(url_for("dev_student"))
    return redirect(url_for("student", name=name))

@app.route("/student/<name>")
def student(name):
    track  = session.get("track", "Unknown Track")
    is_new = session.get("is_new", False)
    return render_template("student.html", content=name, course=track, is_new=is_new)


@app.route('/facilitator')
def facilitator():
    if session.get('user_role') != 'facilitator':
        flash("Please log in as a facilitator to access this page.", "error")
        return redirect(url_for('login'))

    records = (
        db.session.query(Progress, User)
        .join(User, Progress.user_id == User.id)
        .order_by(Progress.completed_at.desc())
        .all()
    )
    return render_template('facilitator.html', progress_records=records)


@app.route("/dev_student")
def dev_student():
    name   = session.get("name", "Student")
    track  = session.get("track", "Software Development")
    is_new = session.get("is_new", False)
    return render_template('dev_student.html', content=name, course=track, is_new=is_new)


@app.route('/course-modules')
def course_modules():
    user_id = session.get("user_id")
    role    = session.get("user_role", "student")

    # Lessons for the data science track
    ds_lessons = ["APIs & Web Scraping", "Introduction to AI"]

    completed = set()
    if user_id:
        records   = Progress.query.filter_by(user_id=user_id).all()
        completed = {r.lesson_name for r in records}

    total       = len(ds_lessons)
    done        = sum(1 for l in ds_lessons if l in completed)
    overall_pct = int((done / total) * 100) if total > 0 else 0

    modules = [
        {
            "number":      1,
            "name":        "APIs & Web Scraping",
            "description": "Learn how to fetch data from web services using APIs and web scraping techniques. Understand authentication, JSON, and practical Python examples.",
            "lessons":     3,
            "hours":       "2.5 hours",
            "route":       "/lesson",
            "completed":   "APIs & Web Scraping" in completed,
        },
        {
            "number":      2,
            "name":        "Introduction to AI",
            "description": "Explore the fundamentals of Artificial Intelligence including deep learning, reinforcement learning, computer vision, NLP, and what makes a great data scientist.",
            "lessons":     7,
            "hours":       "3 hours",
            "route":       "/ai-intro",
            "completed":   "Introduction to AI" in completed,
        },
    ]

    return render_template('course-modules.html', user_role=role,
                           modules=modules, overall_pct=overall_pct)


@app.route('/dev_modules')
def dev_modules():
    user_id = session.get("user_id")

    # Lessons for the software-development track
    dev_lessons = ["SRS Document", "Software Design & UML"]

    completed = set()
    if user_id:
        records   = Progress.query.filter_by(user_id=user_id).all()
        completed = {r.lesson_name for r in records}

    total       = len(dev_lessons)
    done        = sum(1 for l in dev_lessons if l in completed)
    progress_pct = int((done / total) * 100) if total > 0 else 0

    modules = [
        {
            "number":      1,
            "name":        "SRS Document: Software Requirements Specification",
            "description": "Learn how to create your own SRS document for your software prototype.",
            "lessons":     3,
            "hours":       "2.5 hours",
            "route":       "/srs",
            "completed":   "SRS Document" in completed,
        },
        {
            "number":      2,
            "name":        "Software Design",
            "description": "Learn to create designs of a software product before its implementation, and explore different kinds of software designs.",
            "lessons":     7,
            "hours":       "2 hours",
            "route":       "/uml",
            "completed":   "Software Design & UML" in completed,
        },
    ]

    return render_template('dev_modules.html', progress_pct=progress_pct, modules=modules)


# ── Lesson routes ─────────────────────────────────────────────────────────────
def _saved(slug):
    """Return saved lesson content dict or None."""
    row = LessonContent.query.filter_by(slug=slug).first()
    if not row:
        return None
    return {'title': row.title, 'description': row.description,
            'paragraphs': row.get_paragraphs()}


@app.route('/lesson')
def lesson():
    role   = session.get('user_role', 'student')
    is_fac = (role == 'facilitator')
    return render_template('lesson.html', user_role=role, is_facilitator=is_fac,
                           saved_content=_saved('apis-web-scraping'))


@app.route('/ai-intro')
def ai_intro():
    role   = session.get('user_role', 'student')
    is_fac = (role == 'facilitator')
    return render_template('ai-intro.html', user_role=role, is_facilitator=is_fac,
                           saved_content=_saved('intro-ai'))


@app.route('/knowledge-test')
def knowledge_test():
    return render_template('knowledge-test.html')


@app.route('/srs')
def srs():
    role   = session.get('user_role', 'student')
    is_fac = (role == 'facilitator')
    return render_template("srs.html", user_role=role, is_facilitator=is_fac,
                           saved_content=_saved('srs-document'))


@app.route('/uml')
def uml():
    role   = session.get('user_role', 'student')
    is_fac = (role == 'facilitator')
    return render_template('uml.html', user_role=role, is_facilitator=is_fac,
                           saved_content=_saved('software-design-uml'))

@app.route('/admin')
def admin():
    role = session.get('user_role')
    if not role:
        flash("Please log in to continue.", "error")
        return redirect(url_for('login'))
    if role != 'admin':
        return redirect(url_for('facilitator') if role == 'facilitator' else url_for('student', name=session.get('name', '')))

    admin_name = session.get('name', 'Admin')
    total_students    = User.query.filter_by(role='student').count()
    total_facilitators = User.query.filter_by(role='facilitator').count()
    all_users = User.query.filter(User.role != 'admin').order_by(User.role).all()

    return render_template('admin.html',
                           admin_name=admin_name,
                           total_students=total_students,
                           total_facilitators=total_facilitators,
                           all_users=all_users)

# ── Quiz API ──────────────────────────────────────────────────────────────────
@app.route('/api/quiz/submit', methods=['POST'])
def quiz_submit():
    if not session.get('user_id'):
        return jsonify({'error': 'Not logged in'}), 401

    CORRECT = {
        'question1': 'b',   # extract meaningful insights
        'question2': 'a',   # data cleaning and preparation
        'question3': 'a',   # Structured Query Language
        'question4': 'b',   # line chart
        'question5': 'a',   # ensure data quality
    }

    data    = request.get_json(silent=True) or {}
    answers = data.get('answers', {})
    score   = sum(1 for q, a in CORRECT.items() if answers.get(q) == a)
    total   = len(CORRECT)
    percent = int((score / total) * 100)
    return jsonify({'score': score, 'total': total, 'percent': percent})


# ── Lessons API ────────────────────────────────────────────────────────────────
@app.route('/api/lessons/update', methods=['POST'])
def update_lesson():
    if session.get('user_role') != 'facilitator':
        return jsonify({'error': 'Unauthorized'}), 403

    data        = request.get_json(silent=True) or {}
    slug        = data.get('slug', '').strip()
    title       = data.get('title', '').strip()
    description = data.get('description', '').strip()
    paragraphs  = data.get('paragraphs', [])

    if not slug:
        return jsonify({'error': 'Lesson URL identifier is required'}), 400

    row = LessonContent.query.filter_by(slug=slug).first()
    if row:
        if title:       row.title           = title
        if description: row.description     = description
        row.paragraphs_json = json.dumps(paragraphs)
        row.updated_at      = datetime.utcnow()
    else:
        row = LessonContent(slug=slug, title=title, description=description,
                            paragraphs_json=json.dumps(paragraphs))
        db.session.add(row)

    db.session.commit()
    return jsonify({'status': 'ok', 'message': 'Lesson saved successfully.'})


# ── Admin API routes ──────────────────────────────────────────────────────────
@app.route('/api/admin/add-user', methods=['POST'])
def admin_add_user():
    if session.get('user_role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data     = request.get_json(silent=True) or {}
    name     = data.get('name', '').strip()
    email    = data.get('email', '').strip().lower()
    track    = data.get('track', '').strip()
    role     = data.get('role', 'student').strip()
    password = data.get('password', '').strip()

    if not name or not email or not password:
        return jsonify({'error': 'Name, email, and password are required.'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'A user with that email already exists.'}), 409

    new_user = User(name=name, email=email, role=role,
                    track=track if track else None)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'status': 'ok', 'message': f'User {name} created successfully.'})


@app.route('/api/admin/delete-user', methods=['POST'])
def admin_delete_user():
    if session.get('user_role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data  = request.get_json(silent=True) or {}
    email = data.get('email', '').strip().lower()

    if not email:
        return jsonify({'error': 'Email is required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'No user found with that email.'}), 404

    if user.role == 'admin':
        return jsonify({'error': 'Admin accounts cannot be deleted.'}), 403

    Progress.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': 'ok', 'message': f'User {user.name} deleted successfully.'})


# ── Blueprints ────────────────────────────────────────────────────────────────
from routes.auth import auth_bp
from routes.user import user_bp
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(user_bp, url_prefix="/api/user")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
