import sqlite3, json

Database = "test.db"

db = sqlite3.connect(Database, check_same_thread=False)
c=db.cursor()
# please comment the drop tables if not testing
c.executescript(
    """
    drop TABLE Lectures;
    drop TABLE Professor;
    drop TABLE Subject;
    """
)

c.executescript(
    """
    create TABLE if NOT EXISTS Lectures(Lecture_id int primary key, course_title text, lecture_title text, professor_id int, topic text, speed int, vocabulary int);
    create TABLE if NOT EXISTS Professor(professor_id int primary key, professor text, speed int, vocabulary int, stu_interact int);
    create TABLE if NOT EXISTS Subject(topic text, speed text, vocabulary text, stu_interact int);
    """
)

def populate():
    c=db.cursor()
    #assume that when this file is run, database populated from json data
    with open('data_generator/data/courses.json', 'r') as courses_file:
        courses = json.loads(courses_file.read())

    # print('='*50)
    # print(courses)

    with open('data_generator/data/departments.json', 'r') as departments_file:
        departments = json.loads(departments_file.read())

    # print('='*50)
    # print(departments)

    with open('data_generator/data/lectures.json', 'r') as lectures_file:
        lectures = json.loads(lectures_file.read())

    # print('='*50)
    # print(lectures)

    with open('data_generator/data/professors.json', 'r') as professors_file:
        professors = json.loads(professors_file.read())

    # for prof, details in professors.items():
    #     print(prof, details['words']['wpm'])

    # print(list(professors.keys()).index("Mehran Kardar"))
    # lectures["00000"]["instructors"]

    for lec in lectures:
        #no data sanitization here, not because it's not needed, but we trust the json data
        #not sure if type conversion is needed, but added anyways to be safe
        lec_id = int(lec)
        course_name = courses[lectures[f"{lec}"]["course_code"]]["course_title"]
        title = lectures[f"{lec}"]["video_url"].split("/")[-2].replace("-", " ").upper()
        topic = lectures[f"{lec}"]["department"]
        #having instructor id seems extraneous if we have names, but we assign anyways
        #also problem if multiple professors
        prof_id = list(professors.keys()).index(lectures[f"{lec}"]["instructors"][0])
        speed = -1 
        vocab = -1
        #print(lec_id, title, prof_id, topic, speed, vocab)
        #there are some lectures that don't have text analysis available, which is why we check for it
        if (lectures[f"{lec}"]["text_analysis"] != {}):
            speed = round(lectures[f"{lec}"]["text_analysis"]["words"]["wpm"], 2)
            vocab = round(lectures[f"{lec}"]["text_analysis"]["words"]["common_word_ratio"], 2)
        #print(lec_id, title, prof_id, topic, speed, vocab)
        c.execute("INSERT INTO Lectures values (?, ?, ?, ?, ?, ?, ?)", (lec_id, course_name, title, prof_id, topic, speed, vocab))

    for profs in professors:
        prof_id = list(professors.keys()).index(profs)
        name = profs
        speed = round(professors[f"{profs}"]["words"]["wpm"], 2)
        vocab = round(professors[f"{profs}"]["words"]["common_word_ratio"], 2)
        #not sure which value under audience participation to use as student interaction
        #also what is apr
        stu = professors[f"{profs}"]["audience_participation"]["num_audience_participations"]
        # print(prof_id, name, speed, vocab, stu)
        c.execute("INSERT INTO Professor values (?, ?, ?, ?, ?)", (prof_id, name, speed, vocab, stu))
        
    #there are a lot of 0s
    for deps in departments:
        topic = deps
        speed = round(departments[f"{deps}"]["words"]["wpm"], 2)
        vocab = round(departments[f"{deps}"]["words"]["common_word_ratio"], 2)
        stu = departments[f"{deps}"]["audience_participation"]["num_audience_participations"]
        c.execute("INSERT INTO Subject values (?, ?, ?, ?)", (topic, speed, vocab, stu))
        # print(topic, speed, vocab, stu)

    #not sure how to read vtt files, but we may need a module?

    # cursor is closed down here because we want to finish populating database first
    db.commit()
    c.close()

#==========================
# get_all_{table}_data()
def get_all_lecture_data():
    c = db.cursor()
    c.execute("select * from Lectures")
    data = c.fetchall()
    c.close()
    if(data == []):
        return None
    return data

def get_all_professor_data():
    c = db.cursor()
    c.execute("select * from Professor")
    data = c.fetchall()
    c.close()
    if(data == []):
        return None
    return data

def get_all_subject_data():
    c = db.cursor()
    c.execute("select * from Subject")
    data = c.fetchall()
    c.close()
    if(data == []):
        return None
    return data
#==========================

def get_all_lecture_id():
    c = db.cursor()
    c.execute("select Lecture_id from Lectures")
    data = c.fetchall()
    c.close()
    if(data == []):
        return None
    return data


def add_lecture(Lecture_id, lecture_title):
    c = db.cursor()
    c.execute("SELECT MAX(professor_id) FROM Lectures")
    max_id = c.fetchone()
    if (max_id[0] != None):
        new_id = max_id[0] + 1
    else:
        new_id = 0
    #should probably have more arguments, new_id is really the professor id?
    c.execute("insert into Lectures values(?, ?, ?)", (Lecture_id, lecture_title, new_id))
    db.commit()
    c.close()

# ============================== These are used for our search.py
def get_all_lecture_title_and_id(): # Might be useful for searching up lectures by name
    c = db.cursor()
    c.execute("select Lecture_id,lecture_title from Lectures")
    data = c.fetchall()
    c.close()
    if data == None : 
        return []
    Titles = [[Title[0], Title[1]] for Title in data]
    return Titles

def get_all_professor_name_and_id():
    c = db.cursor()
    c.execute("select professor_id,professor from Professor")
    data = c.fetchall()
    c.close()
    if data == None : 
        return []
    Titles = [[Title[0], Title[1]] for Title in data]
    return Titles

def get_all_subjects():
    c = db.cursor()
    c.execute("select topic from Subject")
    data = c.fetchall()
    c.close()
    if data == None : 
        return []
    Titles = [Title[0] for Title in data]
    return Titles
# ==============================

def get_one_lecture_title(Lecture_id): # Maybe not so useful
    c = db.cursor()
    c.execute("select Lecture_title from Lectures where Lecture_id = ?", (Lecture_id))
    data = c.fetchone()
    c.close()
    if(result == None):
        return None
    else: 
        return result[0]

# ==============================
def get_all_professor_id(): # returns a list of all the professor_ids
    c = db.cursor()
    c.execute("select professor_id from Professor")
    data = c.fetchall()
    c.close()
    if data == None : 
        return []
    IDs = [id[0] for id in data]
    return IDs

def get_professor_info(ID): # Gets professor Info by ID
    c = db.cursor()
    c.execute("")
    data = c.fetchall()
    c.close()

populate()