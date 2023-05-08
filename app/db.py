import sqlite3

Database = "test.db"

db = sqlite3.connect(Database, check_same_thread=False)
c=db.cursor()
c.executescript(
    """
    create TABLE if NOT EXISTS Lectures(Lecture_id int primary key, lecture_title text, professor_id int, topic text, speed int, vocabulary int);
    create TABLE if NOT EXISTS Professor(professor_id primary key int, professor text, speed int, vocabulary int, sentiment int, stu_interact int);
    create TABLE if NOT EXISTS Scripts(Lecture_id int, line_id int, line text, time text);
    create TABLE if NOT EXISTS Subject(topic text, speed text, vocabulary text, sentiment text, stu_interact int);
    """
)
c.close()

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
add_lecture(-2,"test_name")