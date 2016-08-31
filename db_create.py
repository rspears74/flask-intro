from project import db
from project.models import BlogPost

# create the database and the db tables
db.create_all()

# INSERT
db.session.add(BlogPost("Good", "Gay homo bitch", 3))
db.session.add(BlogPost("well", "Im gay", 3))
db.session.add(BlogPost("Flask", "discoverflask.com", 3))
db.session.add(BlogPost("postgres", "we setup a local postgres instance", 3))

# commit the changes
db.session.commit()
