from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role          = db.Column(db.String(20), default='student')  # 'student' | 'facilitator'
    track         = db.Column(db.String(60), nullable=True)

    progress = db.relationship('Progress', backref='student', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email} role={self.role}>'


class Progress(db.Model):
    __tablename__ = 'progress'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_name  = db.Column(db.String(120), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'lesson_name', name='uq_user_lesson'),
    )

    def __repr__(self):
        return f'<Progress user={self.user_id} lesson={self.lesson_name}>'


class LessonContent(db.Model):
    __tablename__ = 'lesson_content'

    id              = db.Column(db.Integer, primary_key=True)
    slug            = db.Column(db.String(80), unique=True, nullable=False)
    title           = db.Column(db.String(200))
    description     = db.Column(db.Text)
    paragraphs_json = db.Column(db.Text)   # JSON array of paragraph strings
    updated_at      = db.Column(db.DateTime, default=datetime.utcnow)

    def get_paragraphs(self):
        try:
            return json.loads(self.paragraphs_json) if self.paragraphs_json else []
        except Exception:
            return []

    def __repr__(self):
        return f'<LessonContent slug={self.slug}>'
