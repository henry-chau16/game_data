import dash
from dash import html, callback, Input, Output, dcc
from back_end.gamedata.search_engine import SearchEngine
from back_end.dal import SQLsession

dash.register_page(__name__, path="/", name="Home")

# Home page layout
layout = html.Div([
    dcc.Store(id="session-id", storage_type="session"),
    html.Button("Logout", id="logout-button", n_clicks=0),
    html.Div(id="logout-output", style={"margin-top": "10px"}),
    html.Div(id="debug-output"),
    html.H1(id='welcome'),
    dcc.Input(id="login-username", type="text", placeholder="Search Games"),
    html.Div(id="search-results")
])

@callback(
    Output("search-results", "children"),
    Input("url", "pathname"),  # Triggered when user navigates to home
    prevent_initial_call=True
)
def display_data(pathname):
    # Retrieve SQLsession from the Flask session
    #sqlsession = flask_session['sqlsession']
    sqlsession = SQLsession()
    if not sqlsession:
        return "Session expired. Please log in again."

    # Use SearchEngine with the retrieved SQLsession
    
    return f"DONE"

@callback(
    Output("session-id", "clear_data"),
    Output("logout-output", "children"),
    Input("logout-button", "n_clicks"),
    prevent_initial_call=True
)
def logout(n_clicks):
    return True, "Succesfully logged out!"

@callback(
    Output("welcome", "children"),
    Input("session-id", "data"),
)
def welcome(store_data):
    if store_data:
        return f"Welcome {store_data.get('username')}!"
    return dash.no_update