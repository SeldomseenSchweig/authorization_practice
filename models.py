from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import ForeignKey

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)



class User(db.Model):

    __tablename__='users'

    username = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    password= db.Column(db.Text, nullable=False)
    email=db.Column(db.Text, nullable=False )
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    feedback = db.relationship('Feedback', backref="users", cascade="all, delete-orphan")



    @classmethod
    def register(cls, username,password, email,first_name,last_name):
        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)


    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.get_or_404(username)

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False


class Feedback(db.Model):
    __tablename__='feedback'

    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content= db.Column(db.Text, nullable=False)
    user_username = db.Column(db.String(20), ForeignKey('users.username'), nullable=False)
    


# id - a unique primary key that is an auto incrementing integer
# title - a not-nullable column that is at most 100 characters
# content - a not-nullable column that is text
# username - a foreign key that references the username column in the users table






