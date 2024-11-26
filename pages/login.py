import dash
from dash import html, dcc, Input, Output, State, callback
from back_end.accounts import AccountManager
from back_end.dal import SQLsession

# Register the login page
dash.register_page(__name__, path="/login")

# Initialize the SQLsession and AccountManager
sqlsession = SQLsession()  # Ensure this gets replaced with the session passed in app.py
account_manager = AccountManager(sqlsession)

# Layout for the login page
layout = html.Div([
    html.H1("Login Page"),
    dcc.Tabs(id="tabs", value="login", children=[
        dcc.Tab(label="Login", value="login"),
        dcc.Tab(label="Create Account", value="create_account")
    ]),
    html.Div(id="tab-content")
])

# Callbacks for rendering tabs
@callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_tab(tab):
    if tab == "login":
        return html.Div([
            dcc.Input(id="login-username", type="text", placeholder="Username"),
            dcc.Input(id="login-password", type="password", placeholder="Password"),
            html.Button("Login", id="login-button"),
            html.Div(id="login-output", style={"margin-top": "10px"})
        ])
    elif tab == "create_account":
        return html.Div([
            dcc.Input(id="create-username", type="text", placeholder="New Username"),
            dcc.Input(id="create-password", type="password", placeholder="New Password"),
            html.Button("Create Account", id="create-account-button"),
            html.Div(id="create-account-output", style={"margin-top": "10px"})
        ])

# Callback for login functionality
@callback(
    Output("session-id", "data"),
    Output("login-output", "children"),
    Input("login-button", "n_clicks"),
    State("login-username", "value"),
    State("login-password", "value"),
    prevent_initial_call=True
)
def login(n_clicks, username, password):
    if not username or not password:
        return dash.no_update, "Please fill in all fields."

    if account_manager.verifyLogin(username, password):
        # Store user session info in dcc.Store (example: username and logged_in status)
        return {"logged_in": True, "username": username}, "Login successful! Redirecting..."
    else:
        return dash.no_update, "Invalid username or password."

# Callback for account creation functionality
@callback(
    Output("create-account-output", "children"),
    Input("create-account-button", "n_clicks"),
    State("create-username", "value"),
    State("create-password", "value"),
    prevent_initial_call=True
)
def create_account(n_clicks, username, password):
    if not username or not password:
        return "Please fill in all fields."

    if account_manager.searchAccountID(username):
        return "Username already exists. Please choose another."

    try:
        account_manager.createAccount(username, password)
        return "Account successfully created! You can now log in."
    except Exception as e:
        return f"An error occurred: {str(e)}"
