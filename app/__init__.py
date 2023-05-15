'''
goobergang: 
'''

from flask import *
from db import *
from search import *

app = Flask(__name__)
app.secret_key = "temporarykey" #maybe not needed since we dont have logins


@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html", LEC=get_all_lecture_data(), PROF=get_all_professor_data(), SUB=get_all_subject_data())

# This returns results after entering a certain query in the search
@app.route("/result", methods=["GET"])
def result_page():
    searchterm = request.args.get("search")       
    lecture_result = search_title(searchterm)     # [[id, title], [],]
    prof_result = search_prof(searchterm)         # [[id, title], [],]
    subject_result = search_subject(searchterm)   # [id, id, ]
    return render_template("result.html", LECTURE_RESULTS=lecture_result, PROF_RESULTS=prof_result, SUBJECT_RESULTS=subject_result)

@app.route("/lecture/<lecture_id>", methods=["GET"])
def lecture_page(lecture_id):
    return render_template("lecture_info.html", ID=lecture_id)

if __name__ == "__main__":
    app.debug = True
    app.run()