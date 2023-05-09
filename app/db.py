import sqlite3, json

Database = "test.db"

db = sqlite3.connect(Database, check_same_thread=False)
c=db.cursor()
c.executescript(
    """
    create TABLE if NOT EXISTS Lectures(Lecture_id int primary key, lecture_title text, professor_id int, topic text, speed int, vocabulary int);
    create TABLE if NOT EXISTS Professor(professor_id int primary key, professor text, speed int, vocabulary int, sentiment int, stu_interact int);
    create TABLE if NOT EXISTS Scripts(Lecture_id int, line_id int, line text, time text);
    create TABLE if NOT EXISTS Subject(topic text, speed text, vocabulary text, sentiment text, stu_interact int);
    """
)
c.close()

#assume that when this file is run, database populated from json data
with open('data_generator/data/courses.json', 'r') as courses_file:
    courses = json.loads(courses_file.read())

print('='*50)
print(courses)

with open('data_generator/data/departments.json', 'r') as departments_file:
    departments = json.loads(departments_file.read())


print('='*50)
print(departments)

with open('data_generator/data/lectures.json', 'r') as lectures_file:
    lectures = json.loads(lectures_file.read())


print('='*50)
print(lectures)

with open('data_generator/data/professors.json', 'r') as professors_file:
    professors = json.loads(professors_file.read())

for prof, details in professors.items():
    print(prof, details['words']['wpm'])



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

def get_all_lecture_title(): # Might be useful for searching up lectures by name
    c = db.cursor()
    c.execute("select lecture_title from Lectures")
    data = c.fetchall()
    c.close()
    if(data == []):
        return None
    return data

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

# Not sure if we need this
#def get_all_professor_info():

#==============================
# add_lecture(-2,"test_name")