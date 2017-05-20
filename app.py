from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from flask import jsonify
from flask import Response
import json
import requests

app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flask_movies_dev'
app.debug = True
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user' #names the talbe so you can access it without public.tablename.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

#gets us to the form to add users.
#and get all route
@app.route('/')
def index():
    myUsers = User.query.all()
    for user in myUsers:
        print(user)
    return render_template('add_user.html', myUsers=myUsers)

#get by id route
@app.route('/<id>')
def show_user(id):
    user = User.query.filter_by(id=id).first_or_404()
    return render_template('showOne.html', user=user)

#post route
@app.route('/post_user', methods = ['POST'])
def post_user():
    user = User(request.form['username'], request.form['email']) #creates the user
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

#delete route
@app.route('/delete/<id>', methods = ['POST'])
def deleteOne(id):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))


#Api call to weather Undergaround -- renders json object to screen.
@app.route('/apicall', methods = ['GET'])
def apicall():
    r = requests.get('http://api.wunderground.com/api/98df7348c668dee6/conditions/q/CA/Seattle.json')
    responseData = r.json()
    todaysWeather = {}
    todaysWeather["city"] = responseData['current_observation']['display_location']['city']

    todaysWeather["state"] = responseData['current_observation']['display_location']['state']

    todaysWeather["icon_url"] = responseData['current_observation']['icon_url']

    todaysWeather["temp"] = responseData['current_observation']["temp_f"]

    for i in todaysWeather:
        print (i, todaysWeather[i])

    print(todaysWeather)


    return app.response_class(r, content_type='application/json')
    




if __name__ == "__main__":
    app.run()
