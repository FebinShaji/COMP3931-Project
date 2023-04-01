from flask import render_template, flash, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from .forms import *
from .models import *
from app import db, models
from datetime import datetime
import pandas as pd
import json
import plotly
import plotly.express as px
import numpy as np



@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/aboutUs', methods=['GET', 'POST'])
def aboutUs():
    return render_template('aboutUs.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = Login()

    if request.method == 'POST':

        username = request.form.get('Username')
        password = request.form.get('Password')

        user = models.User.query.filter_by(username=username).first()

        if (user == None):
            flash("Please Provide Some Login Details")
            return redirect(url_for('login'))
        elif (check_password_hash(user.password, password) == False):
            flash("Login Details Did Not Match")
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
            flash("This Email Is Already Registered To An Account")
            return redirect(url_for('register'))
        elif checkUser2:
            flash("This Username Is Already Registered To An Account")
            return redirect(url_for('register'))
        elif (password != confirm_password):
            flash("Passwords Didn't Match")
            return redirect(url_for('register'))
        else:            
            user = User(username=username, password=generate_password_hash(
            password, method='pbkdf2:sha256'), firstName=firstName, surName=surName, email=email)
            db.session.add(user)
            db.session.commit()
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
    password2 = request.form['Confirm_Password']
    if password1 != password2:
        return "These Passwords Don't Match"
    else:
        return ""


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if session.get('user') == None:
        return redirect(url_for('home'))
    userId=session.get('user')
    userDetails=models.User.query.filter_by(id=userId)
    return render_template('dashboard.html', title='Dashboard', userDetails=userDetails)


@app.route("/changeUserDetails", methods=["GET"])
def changeUserDetails():
    if session.get('user') == None:
        return redirect(url_for('home'))

    user = User.query.get(session.get('user'))

    response = f"""
    <form hx-put="/updateUserDetails" hx-target="this">
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
        <button class="btn btn-dark" hx-get="/cancel">Cancel</button>
    </form> 
    """

    return response


@app.route("/cancel", methods=["GET"])
def cancel():
    if session.get('user') == None:
        return redirect(url_for('home'))

    user = User.query.get(session.get('user'))

    response = f"""
    <div><label>Username</label>: { user.username }</div>
    <div><label>First Name</label>: { user.firstName }</div>
    <div><label>Last Name</label>: { user.surName }</div>
    <div><label>Email</label>: { user.email }</div>
    <button hx-get="/changeUserDetails" class="btn btn-dark">Click To Edit</button>
    """

    return response


@app.route("/updateUserDetails", methods=["PUT"])
def updateUserDetails():
    if session.get('user') == None:
        return redirect(url_for('home'))

    user = User.query.get(session.get('user'))

    username = request.form["Username"]
    user.firstName = request.form["firstName"]
    user.surName = request.form["lastName"]
    email = request.form["Email"]
        
    checkUser = models.User.query.filter_by(email=email).first()
    checkUser2 = models.User.query.filter_by(username=username).first()

    if checkUser or checkUser2:
        flash("This Email or Username Is Already Registered To An Account")
    else:
        user.username = username
        user.email = email
    
    db.session.commit()

    response = f"""
    <div><label>Username</label>: { user.username }</div>
    <div><label>First Name</label>: { user.firstName }</div>
    <div><label>Last Name</label>: { user.surName }</div>
    <div><label>Email</label>: { user.email }</div>
    <button hx-get="/changeUserDetails" class="btn btn-dark">Click To Edit</button>
    """

    return response


@app.route('/changePassword', methods=['GET', 'POST'])
def changePassword():

    if session.get('user') == None:
        return redirect(url_for('home'))
    
    response = f"""
    <form hx-put="/updateChangePassword" hx-target="this">
        <div class="field">
            <div class="control">
                <input class="scooteridbox" id="input_text_dashboard" type="Password" name="Password" placeholder="New password">
            </div>
        </div>
        <br>
        <div class="field">
            <div class="control">
                <input class="scooteridbox" id="input_text_dashboard" type="Password" name="Confirm_Password" placeholder="Confirm new password" hx-post="/check-password/" hx-target="#password-err" hx-trigger="keyup">
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


@app.route("/updateChangePassword", methods=["PUT"])
def updateChangePassword():

    if session.get('user') == None:
        return redirect(url_for('home'))
    
    user = models.User.query.get(session.get('user'))

    NewPassword = request.form.get('Password')
    Confirm_NewPassword = request.form.get('Confirm_Password')

    if NewPassword == Confirm_NewPassword:
        user.password = generate_password_hash(NewPassword, method='pbkdf2:sha256')
        db.session.commit()
        response = f"""
        <p class="card-text"><button class="btn btn-dark" hx-get="/changePassword">Forgot your password? Click here to change it.</button></p>
        """

        return response
    else:
        response = f"""
        <p class="card-text"><button class="btn btn-dark" hx-get="/changePassword">Forgot your password? Click here to change it.</button></p>
        """

        return response


@app.route('/workouts', methods=['GET', 'POST'])
def workouts():

    if session.get('user') == None:
        return redirect(url_for('home'))
    
    userId=session.get('user')

    workouts=models.Workout.query.filter_by(userId=userId)

    return render_template('workouts.html', title='Workouts', workouts=workouts)


@app.route("/addWorkouts/", methods=["GET", "POST"])
def addWorkouts():

    if session.get('user') == None:
        return redirect(url_for('home'))
    
    form = Workout()

    userId=session.get('user')

    userDetails=models.User.query.filter_by(id=userId)

    if request.method == 'POST':
        Name = request.form.get('Name')
        Type = request.form.get('Type')
        workout = Workout(userId=userId, name=Name, type=Type)
        db.session.add(workout)
        db.session.commit()
        return redirect(url_for('workouts'))
    
    return render_template('addWorkouts.html', title='addWorkouts', userDetails=userDetails, form=form)


@app.route("/workoutExercises/<int:id>", methods=["GET"])
def workoutExercises(id):

    session['workout'] = id

    if session.get('user') == None:
        return redirect(url_for('home'))
    
    userId=session.get('user')
    workouts=models.Exercise.query.filter_by(userId=userId, workoutId=id)

    return render_template('workoutExercises.html', title='workoutExercises', workouts=workouts)


@app.route("/addExercise", methods=["GET"])
def addExercise():

    userId=session.get('user')
    workoutId=session.get('workout')

    response = f"""
    <form hx-put="/updateAddExercise/{userId}" hx-target="this" class="card-body text-center">
        <div class="text-center">
            <u><p id="thick">Add Your Exercise:</p></u>
        </div>
        <div>
            <label>Exercise Name:</label>
            <input type="text" name="exerciseName">
        </div>
        <button class="btn btn-dark">Submit</button>
        <button class="btn btn-dark" hx-get="/workoutExercises/{workoutId}" hx-target="#here2">Cancel</button>
    </form> 
    <br>
    """

    return response


@app.route("/updateAddExercise/<int:id>", methods=["PUT"])
def updateAddExercise(id):

    userId=session.get('user')
    workoutId=session.get('workout')

    exerciseName = request.form.get('exerciseName')

    exercise = Exercise(userId=userId, workoutId=workoutId, exerciseName=exerciseName)
    db.session.add(exercise)
    db.session.commit()

    response = f"""
    <p>Confirm>
    <button hx-get="/workoutExercises/{workoutId}" hx-target="#here2" class="btn btn-dark">Click To Edit</button>
    """

    return response


@app.route("/delete/<int:id>", methods=["PUT", "GET"])
def delete(id):

    exercise = models.Exercise.query.get(id)

    userId=session.get('user')

    exerciseWeights = models.Exercises.query.filter_by(userId=userId, workoutId=id).all()  

    if (exercise):
        db.session.delete(exercise)
        db.session.commit()
        for el in exerciseWeights:
            db.session.delete(el)
            db.session.commit()

    return redirect("/workoutExercises/" + str(exercise.workoutId))


@app.route("/delete2/<int:id>", methods=["PUT", "GET"])
def delete2(id):

    userId=session.get('user')

    workout = models.Workout.query.get(id)

    exercises = models.Exercise.query.filter_by(userId=userId, workoutId=id).all()
    exerciseWeights = models.Exercises.query.filter_by(userId=userId, workoutId=id).all()  

    if (workout):
        db.session.delete(workout)
        db.session.commit()
        for el in exercises:
            db.session.delete(el)
            db.session.commit()
            for el2 in exerciseWeights:
                db.session.delete(el2)
                db.session.commit()

    return redirect(url_for('workouts'))


@app.route("/delete3/<int:id>", methods=["PUT", "GET"])
def delete3(id):

    exercises = models.Exercises.query.get(id)

    if (exercises):
        db.session.delete(exercises)
        db.session.commit()

    return redirect("/exerciseWeights/" + str(exercises.exerciseId))


@app.route("/exerciseWeights/<int:id>", methods=["GET"])
def exerciseWeights(id):

    if session.get('user') == None:
        return redirect(url_for('home'))
    
    session['exercise'] = id

    userId=session.get('user')
    workoutId=session.get('workout')

    workouts=models.Exercises.query.filter_by(userId=userId, workoutId=workoutId, exerciseId=id).order_by(Exercises.date.desc()).all()

    return render_template('exerciseWeights.html', title='workoutExercises', workouts=workouts, el=id)


@app.route("/addSet/<int:id>", methods=["GET"])
def addSet(id):

    response = f"""
    <form hx-put="/updateAddSet/{id}" hx-target="this">
        <div>
            <label>Date:</label>
            <input type="text" name="Date" placeholder="DD/MM/YYYY">
        </div>
        <div>
            <label>Set 1:</label>
            <input type="text" name="Set1" placeholder="KG">
        </div>
        <div>
            <label>Set 2:</label>
            <input type="text" name="Set2" placeholder="KG">
        </div>
        <div>
            <label>Set 3:</label>
            <input type="text" name="Set3" placeholder="KG">
        </div>
        <div>
            <label>Set 4:</label>
            <input type="text" name="Set4" placeholder="KG">
        </div>
        <button class="btn btn-dark">Submit</button>
        <button class="btn btn-dark" hx-get="/exerciseWeights/{id}" hx-target="#here2">Cancel</button>
    </form>
    <br>
    """

    return response


@app.route("/updateAddSet/<int:id>", methods=["PUT"])
def updateAddSet(id):

    userId=session.get('user')
    workoutId=session.get('workout')

    weightDate = datetime.strptime(request.form.get('Date'), '%d/%m/%Y').date()
    weightSet1 = request.form.get('Set1')
    weightSet2 = request.form.get('Set2')
    weightSet3 = request.form.get('Set3')
    weightSet4 = request.form.get('Set4')

    if weightSet1.isalpha() or weightSet2.isalpha() or weightSet3.isalpha() or weightSet4.isalpha():
        flash("Please make sure only numbers are entered")
    else:
        exercise = Exercises(userId=userId, workoutId=workoutId, exerciseId=id, date=weightDate, set1weight=weightSet1, set2weight=weightSet2, set3weight=weightSet3, set4weight=weightSet4)
        db.session.add(exercise)
        db.session.commit()

    response = f"""
    <p>Confirm>
    <button hx-get="/exerciseWeights/{id}" hx-target="#here2" class="btn btn-dark">Click To Edit</button>
    """

    return response


@app.route("/graphs/<int:id>", methods=["PUT", "GET"])
def graphs(id):

    userId=session.get('user')
    workoutId=session.get('workout')

    workouts=models.Exercises.query.filter_by(userId=userId, workoutId=workoutId, exerciseId=id).order_by(Exercises.date.desc()).all()

    x1 = []
    y1 = []
    for el in workouts:
        z1 = np.array([])
        x1.append(el.date)
        z1 = np.append(z1, el.set1weight)
        z1 = np.append(z1, el.set2weight)
        z1 = np.append(z1, el.set3weight)
        z1 = np.append(z1, el.set4weight)
        y1.append(z1.max())

    df = pd.DataFrame(dict(
        x = x1,
        y = y1
    ))

    fig = px.line(df, x="x", y="y", title="Exercise Weight Progress Chart").update_layout(xaxis_title="Date", yaxis_title="Weight (Kg)")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('graphs.html', graphJSON=graphJSON)


@app.route('/summary', methods=['GET', 'POST'])
def summary():

    userId=session.get('user')

    TotalWorkouts=models.Exercises.query.filter_by(userId=userId).count()

    return render_template('summary.html', el=userId, el2=TotalWorkouts)


@app.route("/addUserWeight", methods=["GET"])
def addUserWeight():

    response = f"""
    <form hx-put="/updateUserWeight" hx-target="this">
        <div>
            <label>Date</label>
            <input type="text" name="Date">
        </div>
        <div>
            <label>Weight:</label>
            <input type="text" name="weight">
        </div>
        <button class="btn btn-dark">Submit</button>
        <button class="btn btn-dark" hx-get="/summary" hx-target="#here2">Cancel</button>
    </form>
    """

    return response


@app.route("/updateUserWeight", methods=["PUT"])
def updateUserWeight():

    userId=session.get('user')

    weightDate = datetime.strptime(request.form.get('Date'), '%d/%m/%Y').date()
    weight = request.form.get('weight')

    weights = UserWeight(userId=userId, date=weightDate, weight=weight)
    db.session.add(weights)
    db.session.commit()

    response = f"""
    <p>COnfirm>
    <button hx-get="/summary" hx-target="#here2" class="btn btn-dark">Click To Edit</button>
    """
    return response


@app.route("/graphs2", methods=["PUT", "GET"])
def graphs2():

    userId=session.get('user')

    weights = models.UserWeight.query.filter_by(userId=userId).order_by(UserWeight.date.desc()).all()

    x1 = []
    y1 = []

    for el in weights:
        x1.append(el.date)
        y1.append(el.weight)

    df = pd.DataFrame(dict(
        x = x1,
        y = y1
    ))

    fig = px.line(df, x="x", y="y", title="Your Weight Progress Chart").update_layout(xaxis_title="Date", yaxis_title="Weight (Kg)")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('graphs.html', graphJSON=graphJSON)