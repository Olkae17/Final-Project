from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['surveyDB']
collection = db['responses']

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'name': request.form.get('name'),
        'age': int(request.form.get('age')),
        'gender': request.form.get('gender'),
        'income': float(request.form.get('income')),
        'expenses': {}
    }

    for category in ['utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare']:
        if request.form.get(category):
            data['expenses'][category] = float(request.form.get(f"{category}_amount", 0))

    collection.insert_one(data)
    return "Submission Successful!"

if __name__ == '__main__':
    app.run(debug=True)
