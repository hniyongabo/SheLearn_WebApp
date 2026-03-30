from flask import Blueprint, request, session, jsonify
from db import db, Progress

user_bp = Blueprint("user", __name__)


@user_bp.route("/progress", methods=["GET"])
def get_progress():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    records = Progress.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "lesson": r.lesson_name,
            "completed_at": r.completed_at.strftime("%Y-%m-%d %H:%M")
        }
        for r in records
    ])


@user_bp.route("/progress", methods=["POST"])
def mark_complete():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data        = request.get_json(silent=True) or {}
    lesson_name = data.get("lesson_name", "").strip()

    if not lesson_name:
        return jsonify({"error": "lesson_name is required"}), 400

    existing = Progress.query.filter_by(user_id=user_id, lesson_name=lesson_name).first()
    if existing:
        return jsonify({"status": "already_complete", "lesson": lesson_name})

    record = Progress(user_id=user_id, lesson_name=lesson_name)
    db.session.add(record)
    db.session.commit()
    return jsonify({"status": "ok", "lesson": lesson_name})
