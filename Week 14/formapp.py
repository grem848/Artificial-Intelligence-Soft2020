# define app that will display submit form and will return personal greeting
from flask import Flask, render_template, request
myapp = Flask(__name__)

@myapp.route('/', methods=['GET', 'POST'])
def index():
    name = None
    if request.method == 'POST' and 'name' in request.form:
        name = request.form['name']
    return render_template('index.html', name=name)

if __name__ == '__main__':
    myapp.run(port=5000, debug=True)
