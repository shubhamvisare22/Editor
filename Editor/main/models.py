from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

# Association table for users and notes
note_users = db.Table(
    "note_users",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("note_id", db.Integer, db.ForeignKey("note.id")),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=True)
    users = db.relationship("User", secondary=note_users, backref="notes")
