# define app that will be deployed on a server and save it in a file
# class ReviewForm(Form):
#    moviereview = TextAreaField('', [validators.DataRequired(), validators.length(min=15)])

# import class Flask
from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import sqlite3
import numpy as np

# load and reuse the pickles
from sklearn.feature_extraction.text import HashingVectorizer
import re
import os
import pickle

cur_dir = os.getcwd()
stop = pickle.load(open(os.path.join('model', 'pickles', 'stopwords.pkl'), 'rb'))

def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text.lower())
    text = re.sub('[\W]+', ' ', text.lower()) \
                   + ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized

# converts document into word vector
vect = HashingVectorizer(decode_error='ignore',
                         n_features=2**21,
                         preprocessor=None,
                         tokenizer=tokenizer)
classifier = pickle.load(open(
                os.path.join('model', 
                'pickles', 
                'classifier.pkl'), 'rb'))

db = os.path.join(os.getcwd(), 'reviews.sqlite')

def classify(document):
    label = {0: 'negative', 1: 'positive'}
    X = vect.transform([document])
    y = classifier.predict(X)[0]
    proba = np.max(classifier.predict_proba(X))
    return label[y], proba

def train(document, y):
    X = vect.transform([document])
    classifier.partial_fit(X, [y])

def sqlite_entry(path, document, y):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO review_db (review, sentiment, date)"\
    " VALUES (?, ?, DATETIME('now'))", (document, y))
    conn.commit()
    conn.close()


# create an instance (our app)
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = None
    if request.method == 'POST' and 'review' in request.form:
        form = request.form['review']
    return render_template('default.html', form=form)


@app.route('/results', methods=['POST'])
def results():
    form = request.form
    if request.method == 'POST':
        review = request.form['review']
        y, proba = classify(review)
        return render_template('results.html', content=review, prediction=y, probability=round(proba*100, 2))
    return render_template('results.html', name=name)

@app.route('/bye', methods=['POST'])
def feedback():
    feedback = request.form['feedback_button']
    review = request.form['review']
    prediction = request.form['prediction']

    inv_label = {'negative': 0, 'positive': 1}
    y = inv_label[prediction]
    if feedback == 'Incorrect':
        y = int(not(y))
    train(review, y)
    sqlite_entry(db, review, y)
    return render_template('bye.html')

if __name__ == '__main__':
    app.run(debug=True)
