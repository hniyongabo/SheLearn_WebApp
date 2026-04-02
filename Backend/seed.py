"""
Run once to populate the database with test data:
    python seed.py

─── Admin ───────────────────────────────────────────────────────────────────
    email:    h@shelearn.bi
    password: admin123

─── Facilitators ────────────────────────────────────────────────────────────
    kankindit@shelearn.io       password: Facilitator2024!
    amara.diallo@shelearn.io    password: Facilitator2024!

─── Students — Software Development (password: Student123!) ─────────────────
    annemu@student.shelearn.io
    claire@student.shelearn.io
    grace.uwera@student.shelearn.io
    fatima.nkusi@student.shelearn.io
    rachel.iradukunda@student.shelearn.io
    alice.mutoni@student.shelearn.io

─── Students — Data Science & Analysis (password: Student123!) ──────────────
    zoe@student.shelearn.io
    diane.uwimana@student.shelearn.io
    nina.habimana@student.shelearn.io
    linda.mukamana@student.shelearn.io
    priya.sharma@student.shelearn.io
    sophie.nzeyimana@student.shelearn.io
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import app
from db import db, User, Progress
from datetime import datetime, timedelta


def seed():
    with app.app_context():
        db.create_all()

        # ── Users ─────────────────────────────────────────────────────────────
        users_data = [
            # Admin
            dict(name="Harmony Naomi Niyongabo",  email="h@shelearn.bi",                         role="admin",       track=None,                    password="admin123"),

            # Facilitators
            dict(name="Dr. Kankindi Tianne",       email="kankindit@shelearn.io",                 role="facilitator", track=None,                    password="Facilitator2024!"),
            dict(name="Amara Diallo",              email="amara.diallo@shelearn.io",              role="facilitator", track=None,                    password="Facilitator2024!"),

            # Software Development students
            dict(name="Anne Mugisha",              email="annemu@student.shelearn.io",            role="student",     track="software-development",  password="Student123!"),
            dict(name="Claire Kaze",               email="claire@student.shelearn.io",            role="student",     track="software-development",  password="Student123!"),
            dict(name="Grace Uwera",               email="grace.uwera@student.shelearn.io",       role="student",     track="software-development",  password="Student123!"),
            dict(name="Fatima Nkusi",              email="fatima.nkusi@student.shelearn.io",      role="student",     track="software-development",  password="Student123!"),
            dict(name="Rachel Iradukunda",         email="rachel.iradukunda@student.shelearn.io", role="student",     track="software-development",  password="Student123!"),
            dict(name="Alice Mutoni",              email="alice.mutoni@student.shelearn.io",      role="student",     track="software-development",  password="Student123!"),

            # Data Science students
            dict(name="Zoe Niyongabo",             email="zoe@student.shelearn.io",               role="student",     track="data-science-analysis", password="Student123!"),
            dict(name="Diane Uwimana",             email="diane.uwimana@student.shelearn.io",     role="student",     track="data-science-analysis", password="Student123!"),
            dict(name="Nina Habimana",             email="nina.habimana@student.shelearn.io",     role="student",     track="data-science-analysis", password="Student123!"),
            dict(name="Linda Mukamana",            email="linda.mukamana@student.shelearn.io",    role="student",     track="data-science-analysis", password="Student123!"),
            dict(name="Priya Sharma",              email="priya.sharma@student.shelearn.io",      role="student",     track="data-science-analysis", password="Student123!"),
            dict(name="Sophie Nzeyimana",          email="sophie.nzeyimana@student.shelearn.io",  role="student",     track="data-science-analysis", password="Student123!"),
        ]

        created = 0
        for data in users_data:
            if not User.query.filter_by(email=data["email"]).first():
                u = User(name=data["name"], email=data["email"],
                         role=data["role"], track=data["track"])
                u.set_password(data["password"])
                db.session.add(u)
                created += 1

        db.session.commit()
        if created:
            print("OK: Created {} new user(s).".format(created))
        else:
            print("All users already exist — skipping user seed.")

        # ── Progress records ───────────────────────────────────────────────────
        # Only seed progress if none exist yet
        if not Progress.query.first():
            def get(email):
                return User.query.filter_by(email=email).first()

            now = datetime.utcnow()

            progress_data = [
                # ── Software Development students ──────────────────────────────
                # Anne — completed both lessons
                Progress(user_id=get("annemu@student.shelearn.io").id,            lesson_name="SRS Document",          completed_at=now - timedelta(days=10)),
                Progress(user_id=get("annemu@student.shelearn.io").id,            lesson_name="Software Design & UML", completed_at=now - timedelta(days=7)),

                # Grace — completed one lesson
                Progress(user_id=get("grace.uwera@student.shelearn.io").id,       lesson_name="SRS Document",          completed_at=now - timedelta(days=4)),

                # Fatima — completed both lessons
                Progress(user_id=get("fatima.nkusi@student.shelearn.io").id,      lesson_name="SRS Document",          completed_at=now - timedelta(days=6)),
                Progress(user_id=get("fatima.nkusi@student.shelearn.io").id,      lesson_name="Software Design & UML", completed_at=now - timedelta(days=3)),

                # Rachel — just started, one lesson done
                Progress(user_id=get("rachel.iradukunda@student.shelearn.io").id, lesson_name="SRS Document",          completed_at=now - timedelta(days=1)),

                # Claire and Alice — no progress (brand new signups)

                # ── Data Science students ──────────────────────────────────────
                # Zoe — completed both lessons
                Progress(user_id=get("zoe@student.shelearn.io").id,               lesson_name="APIs & Web Scraping",   completed_at=now - timedelta(days=8)),
                Progress(user_id=get("zoe@student.shelearn.io").id,               lesson_name="Introduction to AI",    completed_at=now - timedelta(days=5)),

                # Diane — completed both lessons
                Progress(user_id=get("diane.uwimana@student.shelearn.io").id,     lesson_name="APIs & Web Scraping",   completed_at=now - timedelta(days=9)),
                Progress(user_id=get("diane.uwimana@student.shelearn.io").id,     lesson_name="Introduction to AI",    completed_at=now - timedelta(days=6)),

                # Nina — completed one lesson
                Progress(user_id=get("nina.habimana@student.shelearn.io").id,     lesson_name="APIs & Web Scraping",   completed_at=now - timedelta(days=3)),

                # Priya — completed one lesson
                Progress(user_id=get("priya.sharma@student.shelearn.io").id,      lesson_name="APIs & Web Scraping",   completed_at=now - timedelta(hours=20)),

                # Linda and Sophie — no progress yet
            ]

            for p in progress_data:
                db.session.add(p)

            db.session.commit()
            print("OK: Created {} progress records.".format(len(progress_data)))
        else:
            print("Progress records already exist — skipping progress seed.")

        print("\nSeed complete. Summary:")
        print("  Admin accounts:       {}".format(User.query.filter_by(role='admin').count()))
        print("  Facilitator accounts: {}".format(User.query.filter_by(role='facilitator').count()))
        print("  Student accounts:     {}".format(User.query.filter_by(role='student').count()))
        print("  Progress records:     {}".format(Progress.query.count()))
        print("\nYou can now run: python app.py")


if __name__ == "__main__":
    seed()
