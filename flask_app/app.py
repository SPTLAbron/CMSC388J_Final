# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo

# stdlib
import os
from datetime import datetime

# local
from flask_app.forms import CatReviewForm, RegistrationForm, LoginForm, SubmitReview
from flask_app.model import CatClient

# don't change the name
app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://saitheer:saitheer@cluster0.ourpbt0.mongodb.net/CMSC388J?retryWrites=true&w=majority&appName=Cluster0'
app.config['SECRET_KEY'] = "b'\x97\\\xc5X\xa6\xde/\xc1\x05\x8c\x0b\xc3D\xd78\xd8'"
CAT_API_KEY = 'live_VmJ3iTf8cAmyRS1ybiWIv3PeTP0AYLCqlwPJ2KuPQlF5b7j4jRoh80wgQCdg0qTQ'

if os.getenv('MONGO_URI'):
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
if os.getenv('CAT_API_KEY'):
    CAT_API_KEY = os.getenv('CAT_API_KEY')

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

mongo = PyMongo(app)

cat_client = CatClient(CAT_API_KEY, 10)

@app.route('/', methods=['GET', 'POST'])
def index():
    values = cat_client.get_all_cats()
    return render_template('index.html', values=values)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = {
            'username': form.name.data,
            'password': form.text.data,
            'date': current_time()
        }
        mongo.db.catLogins.insert_one(user)
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():    
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.catLogins.find_one({'username': form.username.data})
        if user and user['password'] == form.password.data:
            session['username'] = user['username']
            flash('You have been successfully logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/cats/<cat_id>', methods=['GET', 'POST'])
def cat_detail(cat_id):
    try:
        cat = cat_client.retrieve_cat_by_id(cat_id)
    except ValueError as e:
        flash('Cat not found.', 'error')
        return redirect(url_for('index'))

    review_form = CatReviewForm()
    rating_form = SubmitReview()
    
    if 'username' in session:
        if rating_form.validate_on_submit():
            rating = {
                'cat_id': cat_id,
                'stars': rating_form.stars.data,
                'date': current_time(),
                'user': session['username']
            }
            mongo.db.catRatings.insert_one(rating)
            flash('Your rating has been submitted.', 'success')
            return redirect(url_for('cat_detail', cat_id=cat_id))
    
    if review_form.validate_on_submit():
        review = {
            'cat_id': cat_id,
            'commenter': review_form.name.data,
            'content': review_form.text.data,
            'date': current_time()
        }
        mongo.db.catReviews.insert_one(review)
        return redirect(url_for('cat_detail', cat_id=cat_id))

    reviews = list(mongo.db.catReviews.find({'cat_id': cat_id}))
    ratings = list(mongo.db.catRatings.find({'cat_id': cat_id}))
    
    average_rating = 0.0
    if ratings:
        total_stars = 0
        for rating in ratings:
            print("\n\n\n\n\n\n\n" + rating['stars'])
            total_stars += int(rating['stars'])
        average_rating = round(total_stars / len(ratings), 2)
    
    
    
    return render_template('cat_detail.html', cat=cat, form=review_form, reviews=reviews, ratings=ratings, avg = average_rating, rating_form=rating_form if 'username' in session else None)

# # Not a view function, used for creating a string for the current time.
def current_time() -> str:
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')