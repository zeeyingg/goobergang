'''
goobergang: 
'''

from flask import *
from db import *

app = Flask(__name__)
app.secret_key = "temporarykey" #maybe not needed since we dont have logins


@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html", LEC=get_all_lecture_data(), PROF=get_all_professor_data(), SUB=get_all_subject_data())

@app.route("/result", methods=["GET"])
def result_page():
    return render_template("result.html", searchterm=request.args.get("search"))

if __name__ == "__main__":
    app.debug = True
    app.run()