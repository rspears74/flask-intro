from project import db
from project.models import User

db.session.add(User("randall", "randall@randallspea.rs", "NotGonnaSay"))
db.session.add(User("admin", "ad@min.com", "admin"))

db.session.commit()
