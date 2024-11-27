import pickle
from flask.sessions import SessionInterface, SessionMixin
from uuid import uuid4
from datetime import datetime, timedelta
from back_end.dal import SQLsession, Query


class SQLiteSession(dict, SessionMixin):
    """Custom session class inheriting from Flask's SessionMixin."""
    def __init__(self, session_id, initial=None):
        super().__init__(initial or {})
        self.session_id = session_id
        self.modified = False


class SQLiteSessionInterface(SessionInterface):
    """Custom session interface using SQLite via SQLsession."""
    def __init__(self, db_session: SQLsession, table_name='Sessions'):
        self.session = SQLsession()
        self.table = table_name
        self.query = Query()

    def open_session(self, app, request):
        session_cookie_name = app.config.get("SESSION_COOKIE_NAME", "session")
        session_id = request.cookies.get(session_cookie_name)
        if not session_id:
            session_id = str(uuid4())
            return SQLiteSession(session_id)

        # Retrieve session from SQLite
        command = (
            self.query
            .fields(['data', 'expiration'])
            .source(self.table)
            .where(f' session_id = "{session_id}"')
            .build()
        )
        result = self.session.sql_query(command, fetchall = False)

        if result:
            data, expiration = result
            if datetime.now(datetime.timezone.utc) < datetime.fromisoformat(expiration):
                return SQLiteSession(session_id, pickle.loads(data))

        # If no valid session is found, create a new one
        return SQLiteSession(session_id)

    def save_session(self, app, session, response):
        session_cookie_name = app.config.get("SESSION_COOKIE_NAME", "session") 
        # Remove session if it's empty or expired
        if not session or session.is_empty():
            self.session.sqlDML(f'DELETE FROM {self.table} WHERE session_id = "{session.session_id}"')
            response.delete_cookie(session_cookie_name)
            return

        # Save session to SQLite
        expiration = datetime.now(datetime.timezone.utc) + timedelta(days=1)  # Set expiration
        data = pickle.dumps(dict(session)).hex()

        self.session.sqlDML(f'INSERT OR REPLACE INTO {self.table} (session_id, data, expiration) VALUES ("{session.session_id}", "{data}", "{expiration.isoformat()}")')

        # Set cookie with the session ID
        response.set_cookie(app.session_cookie_name, session.session_id)

