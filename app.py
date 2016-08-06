################
#### import ####
################

from flask import Flask, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os

################
#### config ####
################

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *
from project.users.views import users_blueprint

# register the blueprint
app.register_blueprint(users_blueprint)

##########################
#### helper functions ####
##########################

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You must login first.')
            return redirect(url_for('users.login'))
    return wrap

################
#### routes ####
################

@app.route('/')
@login_required
def home():
    posts = db.session.query(BlogPost).all()
        # return "Hello, World!" # return a string
    return render_template('index.html', posts=posts)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html') # render a template


####################
#### run server ####
####################

if __name__ == '__main__':
    app.run()
