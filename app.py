from flask import Flask , request ,  render_template
from markupsafe import escape
app = Flask(__name__)

@app.route("/")
def home():
     return render_template('index.html')