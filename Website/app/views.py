from flask import render_template, flash, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from .forms import *
from .models import *
from app import db, models

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/aboutUs', methods=['GET', 'POST'])
def aboutUs():
    return render_template('aboutUs.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    print("Logout successful")
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    global result
    result = {}
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        user = models.User.query.filter_by(username=username).first()
        if (user == None):
            flash('Incorrect username or password entered')
            print("Incorrect username or password entered")
            result = {"code": -1, "message": "Incorrect username or password entered"}
            return redirect(url_for('login'))
        elif (check_password_hash(user.password, password) == False):
            flash('Incorrect username or password entered')
            print("Incorrect username or password entered")
            result = {"code": -1, "message": "Incorrect username or password entered"}
            return redirect(url_for('login'))
        else:
            users = models.User.query.filter_by(username = username).all()
            user = users[0]
            session['user'] = user.id
            return redirect(url_for('dashboard'))
        
    return render_template('login.html', title='Log In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    global result
    result = {}
    print('registration started')
    if request.method == 'POST':
        firstName = request.form.get('Firstname')
        surName = request.form.get('Surname')
        email = request.form.get('Email')
        username = request.form.get('Username')
        password = request.form.get('Password')
        confirm_password = request.form.get('Confirm_Password')

        checkUser = models.User.query.filter_by(email=email).first()
        checkUser2 = models.User.query.filter_by(username=username).first()

        if checkUser:
            flash('Account with this email address already exists')
            result = {"code": -1, "message": "Account with this email address already exists"}
            return redirect(url_for('register', methods=['GET', 'POST']))
        elif checkUser2:
            flash('Account with this username already exists')
            result = {"code": -1, "message": "Account with this username already exists"}
            return redirect(url_for('register', methods=['GET', 'POST']))
        else:            
            user = User(username=username, password=generate_password_hash(
            password, method='pbkdf2:sha256'), firstName=firstName, surName=surName, email=email)
            db.session.add(user)
            db.session.commit()
            result = {"code": 0, "message": "Login successful"}
            return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route("/check-username/", methods=['GET', 'POST'])
def check_username():
    username = request.form['Username']
    checkUser = models.User.query.filter_by(username=username).first()
    if checkUser:
        return "That Username Already Exists"
    else:
        return "" 
@app.route("/check-email/", methods=['GET', 'POST'])
def check_email():
    email = request.form['Email']
    checkUser = models.User.query.filter_by(email=email).first()
    if checkUser:
        return "That Email Is Registered To Another Account"
    else:
        return ""
@app.route("/check-password/", methods=['GET', 'POST'])
def check_password():
    password1 = request.form['Password']
    password2 = request.form['Confirm Password']
    if password1 != password2:
        return "These Passwords Don't Match"
    else:
        return ""
    
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    global result
    result = {}
    if session.get('user') == None:
        flash("Need to Login to access")
        return redirect(url_for('home'))
    userId=session.get('user')
    userDetails=models.User.query.filter_by(id=userId)
    return render_template('dashboard.html', title='Dashboard', userDetails=userDetails)

@app.route("/details/<int:id>", methods=["GET"])
def details(id):
    user = User.query.get(id)
    response = f"""
    <form hx-put="/update/{id}" hx-target="this">
        <div>
            <label>Username</label>
            <input type="text" name="Username" value="{user.username}" hx-post="/check-username/" hx-target="#username-err" hx-trigger="keyup">
            <div class="text-danger mt-2" id="username-err"></div>
        </div>
        <div class="form-group">
            <label>First Name</label>
            <input type="text" name="firstName" value="{user.firstName}">
        </div>
        <div class="form-group">
            <label>Last Name</label>
            <input type="text" name="lastName" value="{user.surName}">
        </div>
        <div>
            <label>Email Address</label>
            <input type="email" name="Email" value="{user.email}" hx-post="/check-email/" hx-target="#email-err" hx-trigger="keyup">
            <div class="text-danger mt-2" id="email-err"></div>
        </div>
        <button class="btn btn-dark">Submit</button>
        <button class="btn btn-dark" hx-get="/cancel/{id}">Cancel</button>
    </form> 
    """
    return response

@app.route("/cancel/<int:id>", methods=["GET"])
def cancel(id):
    user = User.query.get(id)

    response = f"""
    <div><label>Username</label>: { user.username }</div>
    <div><label>First Names</label>: { user.firstName }</div>
    <div><label>Last Name</label>: { user.surName }</div>
    <div><label>Email</label>: { user.email }</div>
    <button hx-get="/details/{id}" class="btn btn-dark">Click To Edit</button>
    """
    return response

@app.route("/update/<int:id>", methods=["PUT"])
def update(id):
    user = models.User.query.get(id)
    user.username = request.form["Username"]
    user.firstName = request.form["firstName"]
    user.surName = request.form["lastName"]
    user.email = request.form["Email"]
    db.session.commit()
    
    response = f"""
    <div><label>Username</label>: { user.username }</div>
    <div><label>First Names</label>: { user.firstName }</div>
    <div><label>Last Name</label>: { user.surName }</div>
    <div><label>Email</label>: { user.email }</div>
    <button hx-get="/details/{id}" class="btn btn-dark">Click To Edit</button>
    """
    return response

@app.route('/change_password/<int:id>', methods=['GET', 'POST'])
def changepassword1(id):
    if session.get('user') == None:
        flash("Need to Login to access")
        print("Need to Login to access")
        return redirect(url_for('home'))
    
    response = f"""
    <form hx-put="/update2/{id}" hx-target="this">
        <div class="field">
            <div class="control">
                <input class="scooteridbox" id="input_text_dashboard" type="Password" name="Password" placeholder="New password">
            </div>
        </div>
        <br>
        <div class="field">
            <div class="control">
                <input class="scooteridbox" id="input_text_dashboard" type="Password" name="Confirm Password" placeholder="Confirm new password" hx-post="/check-password/" hx-target="#password-err" hx-trigger="keyup">
                    <div class="text-danger mt-2" id="password-err"></div>
            </div>
        </div>
        <br>
        <div class="field">
            <button class="button btn btn-dark rounded-pill is-block is-info is-fullwidth card-text">Change Password</button>
        </div>
    </form>
    """
    return response

@app.route("/update2/<int:id>", methods=["PUT"])
def update2(id):
    user = models.User.query.get(session.get('user'))
    NewPassword = request.form.get('Password')
    Confirm_NewPassword = request.form.get('Confirm Password')
    if NewPassword == Confirm_NewPassword:
        user.password = generate_password_hash(NewPassword, method='pbkdf2:sha256')
        db.session.commit()
        response = f"""
        <p class="card-text"><button class="btn btn-dark" hx-get="/change_password/{id}">Forgot your password? Click here to change it.</button></p>
        """
        return response
    else:
        flash("The passwords don't match!", 'error')
        response = f"""
        <p class="card-text"><button class="btn btn-dark" hx-get="/change_password/{id}">Forgot your password? Click here to change it.</button></p>
        """
        return response
