from flask import session as flask_session
from flask_session import Session as FlaskSession
from dash import Dash, html, dcc, page_container, page_registry, callback, Input, Output
from back_end.dal import SQLsession, SQLiteSessionInterface
import uuid

def sql_session_gen():
    return SQLsession()

# Initialize Dash app
app = Dash(__name__, use_pages=True)
server = app.server

# Configure Flask sessions
server.config['SECRET_KEY'] = 'supersecretkey'  # Replace with a strong key
server.session_interface = SQLiteSessionInterface(sql_session_gen)
FlaskSession(server)

# App layout
app.layout = html.Div([
    dcc.Store(id="session-id", storage_type="session"),  # Session store
    dcc.Location(id="url", refresh=False),  # For handling redirects
    html.Div([
        dcc.Link(f"{page['name']} - ", href=page['path'])
        for page in page_registry.values()
    ]),
    page_container
])

@callback(
    Output("url", "pathname"),
    Input("session-id", "data"),
    prevent_initial_call=True
)
def handle_redirect(session_data):
    if session_data and session_data.get("logged_in"):
        return "/home"  # Redirect to the home page after login
    return "/login"

@server.route('/init_session')
def initialize_session():
    if 'sqlsession' not in flask_session:
        flask_session['sqlsession'] = SQLsession()
    return "SQLsession initialized!"

if __name__ == "__main__":
    app.run_server(debug=True)
