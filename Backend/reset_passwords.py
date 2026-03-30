"""
Resets all passwords to known values without deleting the database.
Run while Flask is stopped OR while it is running - safe either way.

    python reset_passwords.py

After running:
    h@shelearn.bi                ->  admin123
    kankindit@shelearn.io        ->  Facilitator2024!
    All student accounts         ->  Student123!
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import app
from db import db, User, Progress
from datetime import datetime, timedelta


def reset():
    with app.app_context():

        # ── Reset / create admin ──────────────────────────────────
        admin = User.query.filter_by(email="h@shelearn.bi").first()
        if not admin:
            admin = User(name="Harmony Naomi Niyongabo", email="h@shelearn.bi",
                         role="admin", track=None)
            db.session.add(admin)
            print("Admin user created: h@shelearn.bi")
        admin.set_password("admin123")
        print("Admin password set:     h@shelearn.bi / admin123")

        # ── Reset / create facilitator ────────────────────────────
        fac = User.query.filter_by(email="kankindit@shelearn.io").first()
        if not fac:
            fac = User(name="Dr. Kankindi Tianne", email="kankindit@shelearn.io",
                       role="facilitator", track=None)
            db.session.add(fac)
        fac.set_password("Facilitator2024!")
        print("Facilitator password reset: kankindit@shelearn.io / Facilitator2024!")

        # ── Reset passwords for all students ─────────────────────
        students = User.query.filter_by(role="student").all()
        for s in students:
            s.set_password("Student123!")
            print("Student password reset: {} / Student123!".format(s.email))

        db.session.commit()

        # ── Add progress for first two students if none exist ─────
        if not Progress.query.first() and len(students) >= 2:
            anne = User.query.filter_by(email="annemu@student.shelearn.io").first() or students[0]
            zoe  = User.query.filter_by(email="zoe@student.shelearn.io").first()    or students[1]
            records = [
                Progress(user_id=anne.id, lesson_name="SRS Document",          completed_at=datetime.utcnow() - timedelta(days=5)),
                Progress(user_id=anne.id, lesson_name="Software Design & UML", completed_at=datetime.utcnow() - timedelta(days=2)),
                Progress(user_id=zoe.id,  lesson_name="APIs & Web Scraping",   completed_at=datetime.utcnow() - timedelta(days=3)),
                Progress(user_id=zoe.id,  lesson_name="Introduction to AI",    completed_at=datetime.utcnow() - timedelta(hours=10)),
            ]
            for r in records:
                db.session.add(r)
            db.session.commit()
            print("Added {} dummy progress records.".format(len(records)))

        print("\nDone. Login credentials are ready.")


if __name__ == "__main__":
    reset()
