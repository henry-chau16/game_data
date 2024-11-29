import dash
from dash import html, callback, Input, Output, dcc, State, ctx
from back_end.gamedata.search_engine import SearchEngine
from back_end.dal import SQLsession
from back_end.accounts import ReviewManager, AccountManager

dash.register_page(__name__, path="/home", name="Home")

sqlsession = SQLsession()
search_engine = SearchEngine(sqlsession)
review_manager = ReviewManager(sqlsession)
account_manager = AccountManager(sqlsession)


# Home page layout
layout = html.Div([
    dcc.Store(id="session-id", storage_type="session"),
    dcc.Store(id="game-title", storage_type="session"),
    dcc.Location(id='url', refresh=True),
    html.Button("Logout", id="logout-button", n_clicks=0),
    html.Div(id="logout-output", style={"margin-top": "10px"}),
    html.Div(id="debug-output"),
    html.H1(id='welcome'),
    dcc.Tabs(id="tabs-home", value="search", children=[
        dcc.Tab(label="Search Games", value="search"),
        dcc.Tab(label="Your Reviews", value="get_reviews")
    ]),
    html.Div(id="content")
    
])

@callback(
    Output("content", "children"),
    Input("tabs-home", "value"),
    Input("session-id", "data")
)
def render_tab_home(tab, session_data):
    if tab == "search":
        return html.Div([
            dcc.Input(id="search-query", type="text", placeholder="Search Games"),
            html.Button("Search", id="search-button"),
            html.Div(id="search-results"),
        ])
    elif tab == "get_reviews":
        id = account_manager.searchAccountID(session_data.get('username'))
        reviews = review_manager.getUserReviews(id)
        print(reviews)
        if not reviews:
            reviews = [('None', '')]
        return [
            html.Div(
                [
                    html.H4(f'Game: {item[0]}'),
                    html.P(item[1]),
                ],
                style={"border": "1px solid black", "margin": "10px", "padding": "10px"}
            )
            for item in reviews
        ]

@callback(
    Output("search-results", "children"),
    Input("search-button", "n_clicks"),
    State("search-query", "value"),
    prevent_initial_call=True
)
def display_data(n_clicks, search_query):
    if not search_query:
        return dash.no_update
    results = search_engine.search('Title', search_query, 'TEXT', ['Title', 'ReleaseDate', 'Rating'])
    if not results:
        return html.P(f'No matches for "{search_query}"')
    return [
            html.Div(
                [
                    html.H4(f'Game: {item[0]} Release Date: {item[1]} Rating: {item[2]}'),
                    html.Button("Details", id={"type": "details-button", "index": item[0]})
                ],
                style={"border": "1px solid black", "margin": "10px", "padding": "10px"}
            )
            for item in results
        ]

@callback(
        Output("game-title", "data"),
        Output("url", "pathname", allow_duplicate=True),
        Input({"type": "details-button", "index": dash.ALL}, "n_clicks"),
        State({"type": "details-button", "index": dash.ALL}, "id"),
        prevent_initial_call=True
)
def details(n_clicks, id):
    if not ctx.triggered:
        return dash.no_update, dash.no_update
    else:
        print('details called')
        button_id= ctx.triggered_id
        if button_id and n_clicks[id.index(button_id)]:
            print('going to details', button_id['index'])
            title = button_id['index']
            return {"title": title}, "/details"
        else:
            return dash.no_update, dash.no_update

@callback(
    Output("session-id", "clear_data", allow_duplicate=True),
    Output("logout-output", "children"),
    Output("url", "pathname", allow_duplicate=True),
    Input("logout-button", "n_clicks"),
    prevent_initial_call=True
)
def logout(n_clicks):
    return True, "Succesfully logged out!", "/"

@callback(
    Output("welcome", "children"),
    Input("session-id", "data")
)
def welcome(store_data):
    if store_data:
        return f"Welcome {store_data.get('username')}!"
    return dash.no_update