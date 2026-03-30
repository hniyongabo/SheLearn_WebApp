"""
Run once to create tables and populate dummy data:
    python seed.py

Admin login:
    email:    h@shelearn.bi
    password: admin123

Facilitator login:
    email:    kankindit@shelearn.io
    password: Facilitator2024!

Student logins (all share the same password: Student123!):
    annemu@student.shelearn.io   (Software Development)
    zoe@student.shelearn.io      (Data Science & Analysis)
    claire@student.shelearn.io   (Software Development)
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
            dict(name="Harmony Naomi Niyongabo", email="h@shelearn.bi",               role="admin",       track=None,                    password="admin123"),
            dict(name="Dr. Kankindi Tianne",     email="kankindit@shelearn.io",        role="facilitator", track=None,                    password="Facilitator2024!"),
            dict(name="Anne Mugisha",            email="annemu@student.shelearn.io",   role="student",     track="software-development",  password="Student123!"),
            dict(name="Zoe Niyongabo",           email="zoe@student.shelearn.io",      role="student",     track="data-science-analysis", password="Student123!"),
            dict(name="Claire Kaze",             email="claire@student.shelearn.io",   role="student",     track="software-development",  password="Student123!"),
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
            print("All users already exist - skipping user seed.")

        # ── Dummy progress ─────────────────────────────────────────────────────
        # Claire has NO progress records - she represents a brand-new signup.
        # Any real user who signs up through the form also starts with zero
        # progress records. Lessons only appear after clicking "Mark as Complete".
        if not Progress.query.first():
            anne   = User.query.filter_by(email="annemu@student.shelearn.io").first()
            zoe    = User.query.filter_by(email="zoe@student.shelearn.io").first()

            progress_data = [
                # Anne -- software-development track, 2 lessons done
                Progress(user_id=anne.id, lesson_name="SRS Document",          completed_at=datetime.utcnow() - timedelta(days=5)),
                Progress(user_id=anne.id, lesson_name="Software Design & UML", completed_at=datetime.utcnow() - timedelta(days=2)),
                # Zoe -- data-science-analysis track, 2 lessons done
                Progress(user_id=zoe.id,  lesson_name="APIs & Web Scraping",   completed_at=datetime.utcnow() - timedelta(days=3)),
                Progress(user_id=zoe.id,  lesson_name="Introduction to AI",    completed_at=datetime.utcnow() - timedelta(hours=10)),
                # Claire -- no entries: mirrors a student who just signed up
            ]

            for p in progress_data:
                db.session.add(p)

            db.session.commit()
            print("OK: Created {} progress records.".format(len(progress_data)))
        else:
            print("Progress records already exist - skipping progress seed.")

        print("Done. You can now run: python app.py")


if __name__ == "__main__":
    seed()
