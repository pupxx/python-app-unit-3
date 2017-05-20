from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from flask import jsonify
from flask import Response
import json

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

    # def to_json(self):
    #         return dict(id=self.id,
    #             username=self.username,
    #             email=self.email)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    # def serialize(self):
    #    """Return object data in easily serializeable format"""
    #    return {
    #        'id'         : self.id,
    #        'username'   : self.username,
    #        'email'      : self.email
    #    }

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
    db.session.add(user) #adds the user to the db
    db.session.commit() #commits the add
    return redirect(url_for('index'))#must return from the function indicating what to render or redirect.

#delete route
@app.route('/delete/<id>', methods = ['POST'])
def deleteOne(id):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user) #adds the user to the db
    db.session.commit() #commits the delete
    return redirect(url_for('index'))#must return from the function indicating what to render or redirect.




if __name__ == "__main__":
    app.run()
