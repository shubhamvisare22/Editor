from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from logger import Logger
from models import db
from routes import init_routes

# Initialize the app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secret_key"

# Initialize database and socket
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize logger
app_logger = Logger.get_logger("app")


# Log every request
@app.before_request
def log_request():
    app_logger.info(f"Request to {request.path} with method {request.method}")


# Global exception handling
@app.errorhandler(Exception)
def handle_exception(e):
    app_logger.error(f"Exception occurred: {e}", exc_info=True)
    return jsonify({"message": "failure", "error": str(e)}), 500


# Initialize the routes
init_routes(app, socketio)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensuring the app context is active for DB setup
    socketio.run(app, debug=True)
