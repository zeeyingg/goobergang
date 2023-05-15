from db import *

# Searchs all titles by seeing if the search_term is a substring of the titleRETURN: [[lecture_id, title], [. . .], . . .]
def search_title(search_term): 
    data = get_all_lecture_title_and_id()
    searched = []
    for lecture in data:
        if (( search_term.lower() in lecture[1].lower() )):
            searched.append(lecture)
    return searched

def search_prof(search_term):  
    data = get_all_professor_data()
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
# print(search_title("MATH"))
#print(search_title("thermo"))