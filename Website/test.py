import unittest
from flask import url_for, request
from app import app, views, models, db
from datetime import datetime
from werkzeug.security import generate_password_hash



def addInfo():
    models.User.query.delete()
    models.Workout.query.delete()
    models.Exercise.query.delete()
    models.Exercises.query.delete()
    db.session.commit()

    user1 = models.User(username="febin", password=generate_password_hash(
            "febin", method='pbkdf2:sha256'), firstName="Febin", surName="Shaji", email="shaji.febin@yahoo.com")
    user2 = models.User(username="febin1", password="febin1", firstName="Febin", surName="Shaji", email="febinshaji2@gmail.com")
    workout1 = models.Workout(userId=2, name="Workout 1", type="Chest")
    exercise1 = models.Exercise(userId=2, workoutId=1, exerciseName="Dumbbell Press")
    weights1 = models.Exercises(userId=2, workoutId=1, exerciseId=1, date=datetime.strptime('07/03/2023','%d/%m/%Y'), set1weight=23, set2weight=23, set3weight=23, set4weight=23)
    weights2 = models.Exercises(userId=2, workoutId=2, exerciseId=1, date=datetime.strptime('08/03/2023','%d/%m/%Y'), set1weight=23, set2weight=23, set3weight=23, set4weight=23)

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(workout1)
    db.session.add(exercise1)
    db.session.add(weights1)
    db.session.add(weights2)

    db.session.commit()


class RegisterTest(unittest.TestCase):
    def test_register_success(self):
        with app.test_client() as lTestClient:
            response = lTestClient.post('/register', data={
            'Firstname':"Alan",
            'Surname':"Shaji",
            'Email':"alan@gmail.com",
            'Username':"Alan123",
            'Password':"ALsha123",
            'Confirm_Password':"ALsha123"
            })
            print(response.get_data())
            user = models.User.query.filter_by(username="Alan123").first()
            self.assertIsNotNone(user)

    def test_register_failure1(self):
        response = app.test_client().post('/register', data=dict(
            Firstname="",
            Surname="",
            Email="",
            Username="",
            Password="",
            Confirm_Password=""
        ))
        assert views.result["message"] == "Empty Fields"

    def test_register_failure2(self):
        response = app.test_client().post('/register', data=dict(
            Firstname="Alan",
            Surname="Shaji",
            Email="alan4@gmail.com",
            Username="febin",
            Password="ALsha123",
            Confirm_Password="ALsha123"
        ))
        assert views.result["message"] == "Username Registered To Another Account"

    def test_register_failure3(self):
        response = app.test_client().post('/register', data=dict(
            Firstname="Febin",
            Surname="Shaji",
            Email="shaji.febin@yahoo.com",
            Username="Alan12345",
            Password="ALsha123",
            Confirm_Password="ALsha123"
        ))
        assert views.result["message"] == "Email Registered To Another Account"

    def test_register_failure4(self):
        response = app.test_client().post('/register', data=dict(
            Firstname="Febin",
            Surname="Shaji",
            Email="alan2@gmail.com",
            Username="Alan12345",
            Password="ALsha123",
            Confirm_Password="ALsha1234"
        ))
        assert views.result["message"] == "Passwords Didn't Match"


class LoginTest(unittest.TestCase):
    def test_login_success(self):
        response = app.test_client().post('/login', data=dict(
            Username="febin",
            Password="febin",
        ))
        assert views.result["message"] == "Successful Login"

    def test_login_failure1(self):
        response = app.test_client().post('/login', data=dict(
            Username="",
            Password="",
        ))
        assert views.result["message"] == "Make Sure All Fields Are Filled"

    def test_login_failure2(self):
        response = app.test_client().post('/login', data=dict(
            Username="febin",
            Password="febin2",
        ))
        assert views.result["message"] == "Login Details Did Not Match"


class ChangeUserDetailsTest(unittest.TestCase):
    def test_changedetails_success(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/updateUserDetails', data={
                'Username' : 'AlanNew',
                'firstName' : 'AlanNew',
                'lastName' : 'ShajiNew',
                'Email' : 'alannew@gmail.com'
            })
            assert views.result["message"] == "User Details Changed Successfully"
    
    def test_changedetails_failure1(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/updateUserDetails', data={
                'Username' : '',
                'firstName' : '',
                'lastName' : '',
                'Email' : ''
            })
            assert views.result["message"] == "Empty Fields"

    def test_changedetails_failure2(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/updateUserDetails', data={
                'Username' : 'febin',
                'firstName' : 'AlanNew',
                'lastName' : 'ShajiNew',
                'Email' : 'alannew2@gmail.com'
            })
            assert views.result["message"] == "Username Already Exists"

    def test_changedetails_failure3(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/updateUserDetails', data={
                'Username' : 'AlanNew2',
                'firstName' : 'AlanNew',
                'lastName' : 'ShajiNew',
                'Email' : 'shaji.febin@yahoo.com'
            })
            assert views.result["message"] == "Email Already Exists"

    def test_changedetails_failure4(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/updateUserDetails', data={
                'Username' : 'febin',
                'firstName' : 'AlanNew',
                'lastName' : 'ShajiNew',
                'Email' : 'shaji.febin@yahoo.com'
            })
            assert views.result["message"] == "Username/Email Already Exist"


class ChangePasswordTest(unittest.TestCase):
    def test_password_success(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/updateChangePassword', data={
                'Password' : 'alan123',
                'Confirm_Password' : 'alan123'
            })
            assert views.result["message"] == "Password Changed Successfully"

    def test_password_failure1(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/updateChangePassword', data={
                'Password' : '',
                'Confirm_Password' : ''
            })
            assert views.result["message"] == "Empty Fields"

    def test_password_failure2(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/updateChangePassword', data={
                'Password' : 'alan123',
                'Confirm_Password' : 'alan1234'
            })
            assert views.result["message"] == "Passwords Don't Match"


class AddWorkoutTest(unittest.TestCase):
    def test_workout_success(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.post('/addWorkouts/', data=dict(
                Name="Workout2",
                Type="Legs",
            ), follow_redirects=True)
            assert views.result["message"] == "Workout Added Successfully"
    
    def test_workout_failure1(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.post('/addWorkouts/', data=dict(
                Name="",
                Type="",
            ), follow_redirects=True)
            assert views.result["message"] == "Empty Fields"


class AddExerciseTest(unittest.TestCase):
    def test_add_exercise_success(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
                lSess['workout'] = 1
            response = lTestClient.put('/updateAddExercise/94', data={
                'exerciseName': 'Bench Press'
            })
            assert views.result["message"] == "Exercise Added Successfully"

    def test_add_exercise_failure(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
                lSess['workout'] = 1
            response = lTestClient.put('/updateAddExercise/94', data={
                'exerciseName': ''
            })
            assert views.result["message"] == "Exercise Not Added"


class AddWeightTest(unittest.TestCase):
    def test_add_weight_success(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
                lSess['workout'] = 1
            response = lTestClient.put('/updateAddSet/1', data={
                'Date': '10/04/2023',
                'Set1': 25,
                'Set2': 25,
                'Set3': 32,
                'Set4': 39
            })
            assert views.result["message"] == "Weight Added Successfully"

    def test_add_weight_failure1(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
                lSess['workout'] = 1
            response = lTestClient.put('/updateAddSet/1', data={
                'Date': '',
                'Set1': 25,
                'Set2': 25,
                'Set3': 25,
                'Set4': 25
            })
            assert views.result["message"] == "Empty Date Field"
    
    def test_add_weight_failure2(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
                lSess['workout'] = 1
            response = lTestClient.put('/updateAddSet/1', data={
                'Date': '10/04/2023',
                'Set1': 'fjnvf',
                'Set2': 25,
                'Set3': 25,
                'Set4': 25
            })
            assert views.result["message"] == "Wrong Data Type Entered"

    def test_add_weight_failure3(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
                lSess['workout'] = 1
            response = lTestClient.put('/updateAddSet/1', data={
                'Date': '10/04/2023',
                'Set1': '',
                'Set2': '',
                'Set3': '',
                'Set4': ''
            })
            assert views.result["message"] == "Empty Weight Fields"


class DeleteWeightTest(unittest.TestCase):
    def test_delete_weight_success(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/delete3/2')
            assert views.result["message"] == "Weight Deleted Successfully"


class DeleteExerciseTest(unittest.TestCase):
    def test_delete_exercise_success(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/delete/1')
            assert views.result["message"] == "Exercise Deleted Successfully"


class DeleteWorkoutTest(unittest.TestCase):
    def test_delete_workout_success(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/delete2/1')
            assert views.result["message"] == "Workout Deleted Successfully"


class AddBodyWeightTest(unittest.TestCase):
    def test_add_bodyweight_success(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/updateUserWeight', data={
                'Date': '10/04/2023',
                'weight' : 58.6
            })
            assert views.result["message"] == "Body Weight Added Successfully"

    def test_add_bodyweight_failure1(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/updateUserWeight', data={
                'Date': '',
                'weight' : 58.6
            })
            assert views.result["message"] == "Empty Date Field"
    
    def test_add_bodyweight_failure2(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/updateUserWeight', data={
                'Date': '10/03/2023',
                'weight' : ""
            })
            assert views.result["message"] == "Empty Weight Field"

    def test_add_bodyweight_failure3(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.put('/updateUserWeight', data={
                'Date': '10/03/2023',
                'weight' : "jfnv"
            })
            assert views.result["message"] == "Wrong Data Type Entered"



class LogoutTest(unittest.TestCase):
    def test_logout_success(self):
        with app.test_client() as lTestClient:
            with lTestClient.session_transaction() as lSess:
                lSess['user'] = 2
            response = lTestClient.get('/logout')
            assert views.result["message"] == "Logged Out Successfully"

if __name__ == '__main__':
    addInfo()
    unittest.main()