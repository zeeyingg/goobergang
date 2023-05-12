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

@app.route("/result", methods=["GET"])
def result_page():
    searchterm = request.args.get("search")
    lecture_result = search_title(search_term)     # [[id, title], [],]
    prof_result = search_prof(search_term)         # [[id, title], [],]
    subject_result = search_subject(search_term)   # [id, id, ]
    return render_template("result.html", LECTURE_RESULTS=lecture_results, PROF_RESULTS=prof_result, SUBJECT_RESULTS=subject_result)

if __name__ == "__main__":
    app.debug = True
    app.run()