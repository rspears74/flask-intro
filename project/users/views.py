from flask import render_template, redirect, url_for,\
request, flash, Blueprint # pragma: no cover
from flask_login import login_user, login_required,\
logout_user, current_user # pragma: no cover
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
        follow_self = user.follow(user)
        db.session.add(follow_self)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home.home'))
    return render_template('register.html', form=form)


@users_blueprint.route('/user/<username>')
@login_required
def user_profile(username):
    error = None
    profile_user = User.query.filter_by(name=username).first()
    following = False
    if profile_user is not None:
        posts = db.session.query(BlogPost).filter_by(author_id=profile_user.id).order_by(BlogPost.timestamp.desc())
        user_exists = True
        following = current_user.is_following(profile_user)
        own_profile = (current_user.id == profile_user.id)
    else:
        posts = []
        error = "Sorry, we couldn't find a user with that name."
        user_exists = False
    return render_template(
        'profile.html',
        username=username,
        posts=posts,
        error=error,
        user_exists=user_exists,
        following=following,
        own_profile=own_profile
        )


@users_blueprint.route('/user/<username>/follow', methods=['GET', 'POST'])
@login_required
def follow(username):
    error = None
    profile_user = User.query.filter_by(name=username).first()
    if profile_user is not None:
        if not current_user.id == profile_user.id:
            if not current_user.is_following(profile_user):
                new_follow = current_user.follow(profile_user)
                db.session.add(new_follow)
                db.session.commit()
            else:
                flash("You are already following this user.")
    return redirect(url_for('users.user_profile', username=username))


@users_blueprint.route('/user/<username>/unfollow', methods=['GET', 'POST'])
@login_required
def unfollow(username):
    error = None
    profile_user = User.query.filter_by(name=username).first()
    if profile_user is not None:
        if not current_user.id == profile_user.id:
            if current_user.is_following(profile_user):
                remove_follow = current_user.unfollow(profile_user)
                db.session.add(remove_follow)
                db.session.commit()
            else:
                flash("You are already following this user.")
    return redirect(url_for('users.user_profile', username=username))
