from db import *

# Searchs all titles by seeing if the search_term is a substring of the titleRETURN: [[lecture_id, title], [. . .], . . .]
def search_title(search_term): 
    data = get_all_lecture_title_and_id()
    searched = []
    for lecture in data:
        print(" TYPE: ", type(search_term))
        if (( search_term.lower() in lecture[1].lower() )):
            searched.append(lecture)
    return searched

def search_prof(search_term):  
    data = get_all_professor_name_and_id()
    searched = []
    for prof in data:
        if (( search_term.lower() in prof[1].lower() )):
            searched.append(prof)
    return searched

def search_subject(search_term):
    data = get_all_subjects()
    searched = []
    for sub in data:
        if (( search_term.lower() in sub.lower() )):
            searched.append(sub)
    return searched

def create_path(ID):
    ID = str(ID)
    while len(ID) < 5:
        ID = "0" + ID
    return "data_generator/data/transcripts/" + ID + ".vtt"

def get_transcript(ID):
    with open(create_path(ID), 'r') as transcript:
        result = ""
        transcript.readline()
        for line in transcript:
            result += line + "<br>"
        return result
# print(get_transcript(2))
# print(search_title("MATH"))
#print(search_title("thermo"))