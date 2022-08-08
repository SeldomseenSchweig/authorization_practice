from crypt import methods
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)





@app.route('/')
def go_to_register():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_form() :
    """ Show a form that when submitted will register/create a user. 
    This form should accept a username, password, email, first_name, and last_name.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name= form.first_name.data
        last_name= form.last_name.data
        email= form.email.data
        u = User.register(username,password,email, first_name,last_name)
        flash(f"Thank you for registering {u.username}!", "primary")
        db.session.add(u)
        db.session.commit()
        session['user_id'] = u.username
        return redirect(f'/users/{u.username}')

    return render_template('register_form.html', form=form)

@app.route('/secret')
def secret_page():
    """ Returns the text “You made it!”"""

    if 'user_id' not in session:
        flash('You are not authorized for this page', "danger")
        return redirect('/register')
        
    return render_template('secret_page.html')


@app.route('/login', methods=["POST", "GET"])
def login_form():
    """Show a form that when submitted will login a user. This form should accept a username and a password."""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        u = User.authenticate(username, password)
        flash(f"Welcome Back, {u.username}!", "primary")
        session['user_id'] = u.username
        return redirect(f'/users/{u.username}')
    else:
        form.username.errors = ['Invalid username/password.']



    return(render_template('login_form.html', form=form)) 


@app.route('/logout')
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("user_id")
    flash("Successfully logged out", 'primary')

    return redirect("/login")


# GET /users/<username>

@app.route('/users/<username>')
def user_info(username):
    """Shows user info and feedbacks"""
    if 'user_id' not in session and username != session['user_id']:
        flash('You are not authorized for this page', "danger")
        return redirect(f'/users/{username}')
    feedback = Feedback.query.filter_by(user_username=username).all()
    u = User.query.get_or_404(username)
    return render_template('user_info.html', user = u, feedback=feedback)




@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """ Deletes user and all feedbacks by user"""
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    user = User.query.get_or_404(username)
    if user.username == session['user_id']:
        db.session.delete(user)
        db.session.commit()
        session.pop("user_id")
        flash("User deleted!", "info")
        return redirect('/register')
    flash("You don't have permission to do that!", "danger")
    return redirect(f'/users/{username}')


@app.route('/users/<username>/feedback/add', methods=["POST", "GET"])
def create_feedback(username):
    form = FeedbackForm()
    user = User.query.get_or_404(username)
    if 'user_id' not in session:
        flash("You do not have permission to do that!", "danger")
        return redirect('/login')
    if user.username != session['user_id']:
        flash("You don't have permission to do that!", "danger")
        return redirect(f'/users/{username}')
        
    try:
        if form.validate_on_submit:
            content = form.content.data
            title = form.title.data
            feedback = Feedback(title =title,content=content,user_username=username)
            db.session.add(feedback)
            db.session.commit()
            flash("You posted!", "success")
            return redirect(f'/users/{username}')
    except:
        return render_template('feedback_form.html', form=form)

    return render_template('feedback_form.html', form=form)




@app.route('/feedback/<feedback_id>/update')
def update_feedback(feedback_id):
    """returns form autofilled with post"""
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)
    if 'user_id' not in session:
        flash("You do not have permission to do that!", "danger")
        return redirect('/login')
    if feedback.user_username != session['user_id']:
        flash("You don't have permission to do that!", "danger")
        return redirect(f'/users/{feedback.user_username}')
        

    return render_template('update_form.html', form=form)

@app.route('/feedback/<feedback_id>/update', methods=[ "POST"])
def handle_update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm()        
    if form.validate_on_submit:
            feedback.content = form.content.data
            feedback.title = form.title.data
            db.session.commit()
            flash("You Updated!", "success")
            return redirect(f'/users/{feedback.user_username}')


    flash('Something went wrong', "error")
    return redirect('/feedback/<feedback_id>/update')

@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """ Deletes user and all feedbacks by user"""
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    feedback = Feedback.query.get_or_404(feedback_id)
    user = User.query.get(feedback.user_username)

    if feedback.user_username == session['user_id']:
        db.session.delete(feedback)
        db.session.commit()

        flash("Feedback has been deleted!", "sucess")
        return redirect(f'/users/{user.username}')
    flash("You don't have permission to do that!", "danger")
    return redirect(f'/users/{user.username}')











