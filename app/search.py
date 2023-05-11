from db import *

# Searchs all titles by seeing if the search_term is a substring of the titleRETURN: [[lecture_id, title], [. . .], . . .]
def search_title(search_term): 
    data = get_all_lecture_title_and_id()
    searched = []
    for(lecture in data):
        if (search_term in lecture[1]):
            searched.append(lecture)