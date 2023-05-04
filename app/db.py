import sqlite3

Database = "test.db"

db = sqlite3.connect(Database, check_same_thread=False)
c=db.cursor()
c.executescript(
    """
    create TABLE if NOT EXISTS Lectures(Lecture_id int primary key)
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

def add_lecture(Lecture_id):
    c = db.cursor()
    c.execute("insert into Lectures values()")
    c.close()