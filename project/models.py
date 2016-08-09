from project import db
from project import bcrypt


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)


class BlogPost(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, description, author_id, timestamp):
        self.title = title
        self.description = description
        self.timestamp = timestamp
        self.author_id = author_id

    def __repr__(self):
        return '<{}>'.format(self.title, self.description)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = db.relationship("BlogPost", backref="author")
    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return '<name - {}>'.format(self.name)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def follow(self, user):
        self.followed.append(user)
        return self

    def unfollow(self, user):
        self.followed.remove(user)
        return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return BlogPost.query.join(followers,
            (followers.c.followed_id == BlogPost.author_id)).filter(followers.c.follower_id == self.id).order_by(BlogPost.timestamp.desc())
