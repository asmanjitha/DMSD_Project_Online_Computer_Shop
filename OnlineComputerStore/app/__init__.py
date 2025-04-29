from flask import Flask

app = Flask(__name__)
app.secret_key = 'flash_msg_key'

from app import routes, routes_user, routes_admin


