# Flask Note Application

This is a simple Flask-based note-taking application that supports user registration, authentication, CRUD operations for notes, and real-time note editing using WebSockets.

## Application Structure

The application structure is as follows:

```
flask_note_app/
├── app.py                  # Entry point for the Flask application
├── templates/              # HTML templates for rendering views
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── dashboard.html      # Dashboard for notes
│   └── note.html           # Individual note view
├── static/                 # Static files (CSS, JavaScript, images, etc.)
├── models.py               # Database models for `User` and `Note`
├── logger.py               # Centralized logging utility
├── routes.py               # Routes and WebSocket event handlers
├── requirements.txt        # Python dependencies
└── README.md               # Documentation for the application
```

## Features

- **User Authentication**: Secure login and registration functionality.
- **Note Management**: Create, view, edit, and save notes.
- **Real-Time Collaboration**: WebSocket-based real-time note editing.
- **Centralized Logging**: Robust logging for all critical actions and errors.

## Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-SocketIO

Install all dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Running the Application

To start the application, simply run the `app.py` file:

```bash
python app.py
```

The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Logging

Logs are stored in a `log_files/` directory with separate log files for each component (e.g., `routes.log`). The log format includes timestamps, log levels, file paths, line numbers, and messages for better traceability.

## API Endpoints

### User Authentication

- **`GET /`**: Render the login page.
- **`POST /login`**: Authenticate a user.
- **`POST /register`**: Register a new user.
- **`GET /logout`**: Log out the current user.

### Notes Management

- **`GET /dashboard`**: Display the user's dashboard with all notes.
- **`POST /create_note`**: Create a new note.
- **`GET /notes/<int:note_id>`**: View a specific note.
- **`POST /save_note/<int:note_id>`**: Save changes to a note.

### WebSocket Events

- **`join`**: Join a WebSocket room for collaborative editing.
- **`edit_note`**: Update note content in real time.

## Notes

- This application does not use Flask's migration tools. You need to ensure the database is properly set up before running the application.
- WebSocket functionality is powered by Flask-SocketIO for real-time collaboration.

## Contributing

Feel free to modify and improve the application. Submit issues and pull requests for enhancements.

## License

This project is for educational and interview purposes. You may adapt it for your use.
