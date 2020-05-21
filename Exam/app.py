from flask import Flask, render_template, request
import pickle
app = Flask(__name__)

# Load pickled model
with open('dtc_model.pkl', 'rb') as f:
    loaded_model_web = pickle.load(f)
    
@app.route("/")
def hello():
    return "Hello World!" 

@app.route('/predict', methods=['GET', 'POST'])
def index():
    name = "stranger"
    webprediction = "not predicted yet"
    source = ""
    newsstory = ""
    
    if request.method == 'POST' and 'name' in request.form:
        name = request.form['name']
        
    if request.method == 'POST' and 'source' in request.form:
        source = request.form['source']
        
    if request.method == 'POST' and 'newsstory' in request.form:
        newsstory = request.form['newsstory']
        
    if request.method == 'POST' and 'newsstory' in request.form:
        webprediction = loaded_model_web.predict([source + " - " + newsstory])[0]
    
    return render_template('index.html', name=name, webprediction=webprediction, source=source, newsstory=newsstory)

if __name__ == "__main__":
    app.run()
