from flask import (
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
    current_app,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import emit, join_room
from models import db, User, Note
from logger import Logger

log_obj = Logger.get_logger("routes")


# Routes
def init_routes(app, socketio):

    @app.route("/")
    def home():
        try:
            if "user_id" in session:
                return redirect(url_for("dashboard"))
            return render_template("login.html")
        except Exception as e:
            log_obj.error("Error in home route", exc_info=True)
            return jsonify({"message": "failure", "error": str(e)}), 500

    @app.route("/login", methods=["GET", "POST"])
    def login():
        try:
            if request.method == "POST":
                username = request.form["username"]
                password = request.form["password"]
                user = User.query.filter_by(username=username).first()

                if user and check_password_hash(user.password, password):
                    session["user_id"] = user.id
                    session["username"] = user.username
                    log_obj.info(f"User {user.username} authenticated successfully.")
                    return redirect(url_for("dashboard"))
                log_obj.warning(f"Authentication failed for username: {username}")
                return "Invalid credentials", 401

            return render_template("login.html")
        except Exception as e:
            log_obj.error("Error in login route", exc_info=True)
            return jsonify({"message": "failure", "error": str(e)}), 500

    @app.route("/register", methods=["GET", "POST"])
    def register():
        try:
            if request.method == "POST":
                username = request.form["username"]
                password = generate_password_hash(request.form["password"])

                if User.query.filter_by(username=username).first():
                    log_obj.warning(
                        f"Registration failed: User {username} already exists."
                    )
                    return "User already exists", 400

                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                log_obj.info(f"New user registered: {username}")
                return redirect(url_for("login"))

            return render_template("register.html")
        except Exception as e:
            log_obj.error("Error in register route", exc_info=True)
            return jsonify({"message": "failure", "error": str(e)}), 500

    @app.route("/dashboard")
    def dashboard():
        try:
            if "user_id" not in session:
                return redirect(url_for("login"))

            notes = Note.query.all()
            log_obj.info(f"Fetched {len(notes)} notes for dashboard.")
            return render_template("dashboard.html", notes=notes)
        except Exception as e:
            log_obj.error("Error in dashboard route", exc_info=True)
            return jsonify({"message": "failure", "error": str(e)}), 500

    @app.route("/create_note", methods=["POST"])
    def create_note():
        try:
            if "user_id" not in session:
                return redirect(url_for("login"))

            title = request.form["title"]
            note = Note(title=title, content="")
            note.users.append(User.query.get(session["user_id"]))
            db.session.add(note)
            db.session.commit()
            log_obj.info(f"Note created with title: {title}")
            return redirect(url_for("dashboard"))
        except Exception as e:
            log_obj.error("Error in create_note route", exc_info=True)
            return jsonify({"message": "failure", "error": str(e)}), 500

    @app.route("/notes/<int:note_id>")
    def view_note(note_id):
        try:
            if "user_id" not in session:
                return redirect(url_for("login"))

            note = Note.query.get(note_id)
            if not note:
                log_obj.warning(f"Note with ID {note_id} not found.")
                return "Note not found", 404

            log_obj.info(f"Fetched note with ID: {note_id}, Title: {note.title}")
            return render_template("note.html", note=note)
        except Exception as e:
            log_obj.error("Error in view_note route", exc_info=True)
            return jsonify({"message": "failure", "error": str(e)}), 500

    @app.route("/save_note/<int:note_id>", methods=["POST"])
    def save_note(note_id):
        try:
            if "user_id" not in session:
                return (
                    jsonify({"message": "failure", "error": "User not logged in"}),
                    401,
                )

            data = request.get_json()
            new_content = data.get("content")

            note = Note.query.get(note_id)
            if not note:
                log_obj.warning(f"Note with ID {note_id} not found for update.")
                return jsonify({"message": "failure", "error": "Note not found"}), 404

            note.content = new_content
            db.session.commit()
            log_obj.info(f"Note with ID {note_id} updated successfully.")
            return jsonify(
                {
                    "message": "success",
                    "data": {"note_id": note_id, "content": new_content},
                }
            )
        except Exception as e:
            log_obj.error("Error in save_note route", exc_info=True)
            return jsonify({"message": "failure", "error": str(e)}), 500

    # WebSocket Events
    @socketio.on("join")
    def join(data):
        try:
            with current_app.app_context():
                note_id = data["note_id"]
                join_room(note_id)
                log_obj.info(f"User joined note room with ID: {note_id}")
                emit("message", f"User joined note {note_id}", room=note_id)
        except Exception as e:
            log_obj.error("Error in join socket event", exc_info=True)

    @socketio.on("edit_note")
    def edit_note(data):
        try:
            with current_app.app_context():
                note_id = data["note_id"]
                new_content = data["content"]

                note = Note.query.get(note_id)
                if note:
                    note.content = new_content
                    db.session.commit()
                    log_obj.info(f"Note with ID {note_id} updated via WebSocket.")
                    emit(
                        "update_note",
                        {"note_id": note_id, "content": new_content},
                        room=note_id,
                    )
                else:
                    log_obj.warning(
                        f"Note with ID {note_id} not found for WebSocket update."
                    )
                    emit("error", {"message": "Note not found"})
        except Exception as e:
            log_obj.error("Error in edit_note socket event", exc_info=True)

    @app.route("/logout")
    def logout():
        try:
            session.clear()
            log_obj.info("User logged out successfully.")
            return redirect(url_for("login"))
        except Exception as e:
            log_obj.error("Error in logout route", exc_info=True)
            return jsonify({"message": "failure", "error": str(e)}), 500
