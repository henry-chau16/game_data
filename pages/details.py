import dash
from dash import html, callback, Input, Output, dcc, State, callback_context
from back_end.gamedata.search_engine import SearchEngine
from back_end.dal import SQLsession
from back_end.accounts import ReviewManager, AccountManager

dash.register_page(__name__, path="/details", name="Game Details")

sqlsession = SQLsession()
search_engine = SearchEngine(sqlsession)
review_manager = ReviewManager(sqlsession)
account_manager = AccountManager(sqlsession)

layout = html.Div([
    dcc.Store(id="session-id", storage_type="session"),
    dcc.Store(id="game-title", storage_type="session"),
    dcc.Location(id="url", refresh=True),
    html.Button("Logout", id="logout-details-button", n_clicks=0),
    html.Button("Home", id='home-button'),
    html.Div(id="logout-details-output", style={"margin-top": "10px"}),
    html.H1(id='game'),
    dcc.Tabs(id="tabs-game", value="details", children=[
        dcc.Tab(label="About the Game", value="details"),
        dcc.Tab(label="Write a review!", value="write_review")
    ]),
    html.Div(id="game-content")
    
])

@callback(
    Output("session-id", "clear_data", allow_duplicate=True),
    Output("game-title", "clear_data", allow_duplicate=True),
    Output("logout-details-output", "children"),
    Output("url", "pathname", allow_duplicate=True),
    Input("logout-details-button", "n_clicks"),
    prevent_initial_call=True
)
def logout(n_clicks):
    return True, True, "Succesfully logged out!", "/"

@callback(
    Output("game-title", "data", allow_duplicate=True),
    Output("url", "pathname", allow_duplicate=True),
    Input("home-button", "n_clicks"),
    prevent_initial_call=True
)
def go_home(n_clicks):
    return {"title": ''}, "/home"

@callback(
    Output("game", "children"),
    Input("game-title", "data"),
)
def game_name(store_data):
    if store_data:
        return f'{store_data.get("title")}'
    return dash.no_update

@callback(
    Output("game-content", "children"),
    Input("tabs-game", "value"),
    Input("game-title", "data")
)
def render_tab_home(tab, session_data):
    if tab == "details":
        title = session_data.get('title')
        results = search_engine.search('Title', title, 'TEXT', expr = '=', fetchall=False)
        release, teams, rating, genres, summary, playing = results[1], results[2], results[3], results[6], results[7], results[8]
        genre_str, teams_str = genres.replace('[', '').replace(']', '').replace("'", ''), teams.replace('[', '').replace(']', '').replace("'", '')
        reviews = review_manager.fetchReviews(title)
        if not reviews:
            reviews = [('None', '')]

        return[html.Div([
                html.H4(f'Released on {release}'),
                html.H5(f'Rating: {rating}  Playing: {playing}  Genres: {genre_str}'),
                html.H5(f'Teams working on {title}: {teams_str}'),
                html.P(f'Game Summary: {summary}'),
                html.H2("Reviews:")
            ]    
        )] + [
            html.Div(
                [
                    html.H5(f'User: {item[0]}'),
                    html.P(item[1]),

                ],
                style={"border": "1px solid black", "margin": "10px", "padding": "10px"}
            )
            for item in reviews
        ]
    elif tab == "write_review":
        return html.Div([
            dcc.Textarea(
                id='review-text',
                value='',
                style={'width': '50%', 'height': 200},  # Adjust dimensions as needed
            ),
            html.Button("Post", id = "create-review-button"),
            html.Div(id="review-output")
        ])
    
@callback(
    Output("review-output", "children"),
    Input("create-review-button", "n_clicks"),
    State("review-text", "value"),
    Input("session-id", "data"),
    Input("game-title", "data"),
    prevent_initial_call=True
)
def post_review(n_clicks, review_text, session_data, game_data):
    if not review_text:
        return "The review doesn't write itself!"
    id = account_manager.searchAccountID(session_data.get('username'))
    title = title = game_data.get('title')
    try:
        review_manager.createReviews(title, review_text, id)
        return "Review Posted!"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    