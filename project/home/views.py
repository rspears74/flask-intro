################
#### import ####
################

from project import app, db # pragma: no cover
from project.models import BlogPost # pragma: no cover
from flask import render_template, Blueprint, flash, request, redirect,\
url_for # pragma: no cover
from flask_login import login_required, current_user # pragma: no cover
from project.home.form import MessageForm # pragma: no cover
from datetime import datetime # pragma: no cover

################
#### config ####
################

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
) # pragma: no cover


################
#### routes ####
################

@home_blueprint.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    error = None
    form = MessageForm(request.form)
    if form.validate_on_submit():
        new_message = BlogPost(
            form.title.data,
            form.description.data,
            current_user.id,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(new_message)
        db.session.commit()
        flash('New entry was successfully posted. Thanks.')
        return redirect(url_for('home.home'))
    else:
        posts = db.session.query(BlogPost).order_by(BlogPost.timestamp.desc())
        return render_template(
            'index.html',
            posts=posts,
            form=form,
            error=error
        )


@home_blueprint.route('/')
def welcome():
    return render_template('welcome.html')
