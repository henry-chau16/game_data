from dash import Dash, html, dcc, page_container, callback, Input, Output
from back_end.dal import SQLsession, SQLiteSessionInterface


def sql_session_gen():
    return SQLsession()

# Initialize Dash app
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
server = app.server

# Configure Flask sessions
server.config['SECRET_KEY'] = 'supersecretkey'  # Replace with a strong key
server.config['SESSION_TYPE'] = 'filesystem'
server.session_interface = SQLiteSessionInterface(sql_session_gen)


# App layout
app.layout = html.Div([
    dcc.Store(id="session-id", storage_type="session"),  # Session store
    dcc.Location(id="url", refresh=True),  # For handling redirects
    page_container
])

@callback(
    Output("url", "pathname"),
    Input("session-id", "data")
)
def handle_redirect(session_data):
    if session_data and session_data.get("logged_in"):
        return "/"  # Redirect to the home page after login
    return "/login"

if __name__ == "__main__":
    app.run_server(debug=True)
