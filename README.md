App Dependencies: 
-------------------
blinker==1.9.0
cachelib==0.13.0
certifi==2024.8.30
charset-normalizer==3.4.0
click==8.1.7
colorama==0.4.6
dash==2.18.2
dash-core-components==2.0.0
dash-html-components==2.0.0
dash-table==5.0.0
Flask==3.0.3
Flask-Session==0.8.0
idna==3.10
importlib_metadata==8.5.0
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==3.0.2
msgspec==0.18.6
nest-asyncio==1.6.0
numpy==2.1.3
packaging==24.2
pandas==2.2.3
plotly==5.24.1
python-dateutil==2.9.0.post0
pytz==2024.2
requests==2.32.3
retrying==1.3.4
six==1.16.0
tenacity==9.0.0
typing_extensions==4.12.2
tzdata==2024.2
urllib3==2.2.3
Werkzeug==3.0.6
zipp==3.21.0
--------------------

RUNNING THE APP:
----------------------------------------------
Ensure you are in the app root directory:
cd <path-to-game_data-folder>/game_data/

Activate virtual environment:
app_env\Scripts\activate

Or if installing dependencies manually:
pip install -r requirements.txt

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
IF DATABASE FILE IS NOT IN APP ROOT DIRECTORY OR FIRST TIME RUNNING THE APP:
python server_init.py

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Run app.py:
set FLASK_APP=app.py 
flask run
***
Running app using just python app.py will cause callback errors with flask elements in session storage
***

-------------------------------------------------
App will be hosted on a local port:
http://127.0.0.1:8050/ (by default)

