from flask import render_template, redirect, url_for,\
request, flash, Blueprint # pragma: no cover
from flask_login import login_user, login_required,\
logout_user # pragma: no cover
from project.users.form import LoginForm, RegisterForm # pragma: no cover
from project.models import User, BlogPost, bcrypt # pragma: no cover
from project import db # pragma: no cover

################
#### config ####
################

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
) # pragma: no cover


################
#### routes ####
################

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(
                    user.password,
                    request.form['password']):
                login_user(user)
                flash('You were logged in.')
                return redirect(url_for('home.home'))
            else:
                error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('home.welcome'))


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home.home'))
    return render_template('register.html', form=form)


@users_blueprint.route('/user/<username>')
@login_required
def user_profile(username):
    error = None
    profile_user = User.query.filter_by(name=username).first()
    if profile_user is not None:
        posts = db.session.query(BlogPost).filter_by(author_id=profile_user.id).order_by(BlogPost.timestamp.desc())
    else:
        posts = []
        error = "Sorry, we couldn't find a user with that name."
    return render_template(
        'profile.html',
        username=username,
        posts=posts,
        error=error
        )
