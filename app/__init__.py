'''
goobergang: 
'''

from flask import Flask
from flask import render_template
from flask import request
from db import *
from search import *
import json

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

@app.route("/professor", methods=["GET"])
def professor_page():
    #lecture_data = json.dumps(lecture_data_json())
    prof_data = json.dumps(prof_data_json())
    #dep_data = json.dumps(dep_data_json())
    return render_template("professor.html", data = prof_data)

@app.route("/lecture", methods=["GET"])
def lecture_page():
    return render_template("lecture.html")

@app.route("/departments", methods=["GET"])
def department_page():
    lecture_data = json.dumps(lecture_data_json())
    prof_data = json.dumps(prof_data_json())
    dep_data = json.dumps(dep_data_json())
    return render_template("departments.html", data1=lecture_data, data2=prof_data, data3=dep_data)

@app.route("/lecture/<lecture_id>", methods=["GET"])
def lecture_info(lecture_id):
    return render_template("lecture_info.html", ID=lecture_id)

@app.route("/prof/<prof_id>", methods=["GET"])
def prof_info(prof_id):
    prof_lectures = get_lectures_from_prof_id(prof_id)

    info = get_professor_info(prof_id)[0]
    s=info[2] # Speed
    v=info[3] # vocab
    i=info[4] # student interaction

    return render_template("prof_info.html", ID=prof_id, LECTURES=prof_lectures, SPEED=s, VOCAB=v, INTERACTION=i)

@app.route("/subject/<subject>", methods=["GET"])
def subject_info(subject):
    return render_template("subject_info.html", ID=subject)

@app.route("/d3test")
def d3test():
    lecture_data = json.dumps(lecture_data_json())
    prof_data = json.dumps(prof_data_json())
    dep_data = json.dumps(dep_data_json())
    return render_template("d3test.html", data1=lecture_data, data2=prof_data, data3=dep_data)

if __name__ == "__main__":
    app.debug = True
    app.run()