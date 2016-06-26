from app import db
from models import BlogPost

# create the database and the db tables
db.create_all()

# INSERT
db.session.add(BlogPost("Good", "Gay homo bitch"))
db.session.add(BlogPost("well", "Im gay"))
db.session.add(BlogPost("Flask", "discoverflask.com"))
db.session.add(BlogPost("postgres", "we setup a local postgres instance"))

# commit the changes
db.session.commit()
