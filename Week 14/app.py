# define app that will be deployed on a server and save it in a file

# import class Flask
from flask import Flask

# create an instance (our app)
app = Flask(__name__)

# by default, Flask server runs on http://127.0.0.1:5000
# we define relative URL on the server, where our app will be hosted - binds it to the URL
@app.route('/app')
def hello():
    return 'Hello, Flask!'

if __name__ == '__main__' :
    app.run(port=5000,debug=True);
    
