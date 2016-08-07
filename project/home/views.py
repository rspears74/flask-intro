################
#### import ####
################

from project import app, db
from project.models import BlogPost
from flask import render_template, Blueprint, flash, request, redirect,\
url_for
from flask_login import login_required, current_user
from project.home.form import MessageForm

################
#### config ####
################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)


################
#### routes ####
################

@home_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def home():
    error = None
    form = MessageForm(request.form)
    if form.validate_on_submit():
        new_message = BlogPost(
            form.title.data,
            form.description.data,
            current_user.id
        )
        db.session.add(new_message)
        db.session.commit()
        flash('New entry was successfully posted. Thanks.')
        return redirect(url_for('home.home'))
    else:
        posts = db.session.query(BlogPost).all()
        return render_template(
            'index.html',
            posts=posts,
            form=form,
            error=error
        )


@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')
