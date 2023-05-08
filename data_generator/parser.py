# I really need to write comments on this but will get to that l8r
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import webvtt
import json
import time

department_ids = {
	'1': 'Civil and Environmental Engineering',
	'2': 'Mechanical Engineering',
	'3': 'Materials Science and Engineering',
	'4': 'Architecture',
	'5': 'Chemistry',
	'6': 'Electrical Engineering and Computer Science',
	'7': 'Biology',
	'8': 'Physics',
	'9': 'Brain and Cognitive Sciences',
	'10': 'Chemical Engineering',
	'11': 'Urban Studies and Planning',
	'12': 'Earth, Atmospheric, and Planetary Sciences',
	'14': 'Economics',
	'15': 'Management',
	'16': 'Aeronautics and Astronautics',
	'17': 'Political Science',
	'18': 'Mathematics',
	'20': 'Biological Engineering',
	'21': 'Humanities',
	'21A': 'Anthropology',
	'21H': 'History',
	'21G': 'Global Languages',
	'21L': 'Literature',
	'21M': 'Music and Theater Arts',
	'21W': 'Writing',
	'22': 'Nuclear Science and Engineering',
	'24': 'Linguistics and Philosophy',
	'CMS': 'Comparative Media Studies/Writing',
	'EC': 'Edgerton Center',
	'ES': 'Experimental Study',
	'ESD': 'Engineering Systems Division',
	'HST': 'Health Sciences and Technology',
	'MAS': 'Media Arts and Sciences',
	'CC': 'Concourse',
	'IDS': 'Institute for Data, Systems, and Society',
	'PE': 'Phys. Ed.',
	'WGS': "Women's and Gender Studies",
	'STS': 'Science, Technology, and Society',
	'RES': 'Supplemental Resources'
} # I think this is complete!

ranked_words = {}

with open('data/ranked_words.json', 'r') as ranked_words_file:
	ranked_words = json.loads(ranked_words_file.read())

def generate_course_catalog(in_path='data/course_catalog.html', out_path='data/courses.json'):
	catalog_html = open(in_path, 'r').read()
	soup = BeautifulSoup(catalog_html, 'html.parser')

	courses = soup.findAll('div', {'class': 'lr-info'})
	courses_dict = {}

	for index, course in enumerate(courses):
		details = course.findChildren()

		course_code = details[0].text
		title = details[1].text
		level = details[4].text
		url = 'https://ocw.mit.edu' + details[2]['href']
		department = get_department_from_course_code(course_code)
		print(f"Doing {course_code}: {title} ({index+1} / {len(courses)})")
		lectures = get_lecture_urls(url)

		courses_dict[course_code] = {
			'course_title': title,
			'course_department': department,
			'course_url': url,
			'course_level': level,
			'course_lectures': lectures
		}

	with open(out_path, 'w') as f:
		out_json = json.dumps(courses_dict, indent=4)

		f.write(out_json)

def generate_lecture_ids(in_path='data/courses.json', out_path='data/lectures.json'):
	with open(in_path, 'r') as f:
		lectures = json.loads(f.read())

	with open(out_path, 'w') as f:
		f.write('{}')

	counter = 0
	lecture_ids = {}

	for course_code in lectures:
		for video_url in lectures[course_code]['course_lectures']:
			lecture_id = str(counter).zfill(5)
			html = requests.get(video_url).text

			instructors, caption_url = get_lecture_info(html)
			department = get_department_from_course_code(course_code)
			generate_transcript(lecture_id, caption_url)
			text_analysis = get_rhetorical_style_from_lecture_id(lecture_id)

			lecture_ids[lecture_id] = {
				'video_url': video_url,
				'department': department,
				'course_code': course_code,
				'instructors': instructors,
				'caption_url': caption_url,
				'text_analysis': text_analysis
			}
			print(lecture_ids[lecture_id])

			counter += 1

	with open(out_path, 'w') as f:
		f.write(json.dumps(lecture_ids, indent=4))

def generate_transcript(lecture_id, transcript_url, out_path='data/transcripts/'):
	print(f"Doing {lecture_id}...")
	if not transcript_url:
		return
		
	transcript = requests.get(transcript_url).text

	with open(f'{out_path}{lecture_id}.vtt', 'w') as f:
		f.write(transcript)

	print(f"Finished {lecture_id}!\n")

def generate_professors(in_path='data/lectures.json', out_path='data/professors.json'):
	professors = {}

	with open(in_path, 'r') as lectures_file:
		lectures = json.loads(lectures_file.read())

	for lecture_id in lectures:
		instructors = lectures[lecture_id]['instructors']
		course_code = lectures[lecture_id]['course_code']

		for instructor in instructors:
			if not(instructor in professors):
				professors[instructor] = {
					'total_duration': 0,
					'total_chars': 0,
					'words': {
						'num_words': 0,
						'num_common_words': 0
					},
					'sentences': {
						'num_sents': 0,
						'num_qmarks': 0
					},
					'audience_participation': {
						'num_audience_participations': 0
					},
					'lectures': [],
					'courses': []
				}

			print(lecture_id)
			print(lectures[lecture_id]['text_analysis'])
			print()
			text_analysis = lectures[lecture_id]['text_analysis']

			if not text_analysis:
				continue

			professors[instructor]['total_duration'] += text_analysis['duration']
			professors[instructor]['total_chars'] += text_analysis['num_chars']
			professors[instructor]['words']['num_words'] += text_analysis['words']['num_words']
			professors[instructor]['words']['num_common_words'] += text_analysis['words']['num_common_words']
			professors[instructor]['sentences']['num_sents'] += text_analysis['sentences']['num_sents']
			professors[instructor]['sentences']['num_qmarks'] += text_analysis['sentences']['num_qmarks']
			professors[instructor]['audience_participation']['num_audience_participations'] += text_analysis['audience_participation']['num_audience_participations']
			professors[instructor]['lectures'].append(lecture_id)

			if not(course_code in professors[instructor]['courses']):
				professors[instructor]['courses'].append(course_code)

	for prof in professors:
		if professors[prof]['total_duration'] > 0:
			professors[prof]['words']['wpm'] = (professors[prof]['words']['num_words'] / professors[prof]['total_duration']) * 60
			professors[prof]['sentences']['qmarks_per_hour'] = (professors[prof]['sentences']['num_qmarks'] / professors[prof]['total_duration']) * 3600
			professors[prof]['audience_participation']['apr'] = (professors[prof]['audience_participation']['num_audience_participations'] / professors[prof]['total_duration']) * 3600
		else:
			professors[prof]['words']['wpm'] = 0
			professors[prof]['sentences']['qmarks_per_hour'] = 0
			professors[prof]['audience_participation']['apr'] = 0

		if professors[prof]['words']['num_words'] > 0:
			professors[prof]['words']['avg_word_length'] = professors[prof]['total_chars'] / professors[prof]['words']['num_words']
			professors[prof]['words']['common_word_ratio'] = professors[prof]['words']['num_common_words'] / professors[prof]['words']['num_words']
		else:
			professors[prof]['words']['avg_word_length'] = 0
			professors[prof]['words']['common_word_ratio'] = 0

		if professors[prof]['sentences']['num_sents'] > 0:
			professors[prof]['sentences']['avg_words_per_sent'] = professors[prof]['words']['num_words'] / professors[prof]['sentences']['num_sents']
		else:
			professors[prof]['sentences']['avg_words_per_sent'] = 0

	with open(out_path, 'w') as professors_file:
		professors_file.write(json.dumps(professors, indent=4))

def generate_departments(out_path='data/departments.json'):
	departments = {}

	for dept_id in department_ids:
		dept_name = department_ids[dept_id]
		departments[dept_name] = {
			'total_duration': 0,
			'total_chars': 0,
			'words': {
				'num_words': 0,
				'num_common_words': 0
			},
			'sentences': {
				'num_sents': 0,
				'num_qmarks': 0
			},
			'audience_participation': {
				'num_audience_participations': 0
			},
			'lecturers': [],
			'courses': [],
			'lectures': []
		}

	with open('data/courses.json', 'r') as courses_file:
		courses = json.loads(courses_file.read())

	for course_id in courses.keys():
		course_dept = courses[course_id]['course_department']

		if course_dept == 'N/A':
			continue

		departments[course_dept]['courses'].append(course_id)

	with open('data/lectures.json', 'r') as lectures_file:
		lectures = json.loads(lectures_file.read())

	for lecture_id in lectures.keys():
		lecture_dept = lectures[lecture_id]['department']
		instructors = lectures[lecture_id]['instructors']
		text_analysis = lectures[lecture_id]['text_analysis']

		if not text_analysis:
			continue

		if lecture_dept == 'N/A':
			continue

		departments[lecture_dept]['lectures'].append(lecture_id)
		departments[lecture_dept]['lecturers'] = list(set(departments[lecture_dept]['lecturers'] + instructors))
		departments[lecture_dept]['total_duration'] += text_analysis['duration']
		departments[lecture_dept]['total_chars'] += text_analysis['num_chars']
		departments[lecture_dept]['words']['num_words'] += text_analysis['words']['num_words']
		departments[lecture_dept]['words']['num_common_words'] += text_analysis['words']['num_common_words']
		departments[lecture_dept]['sentences']['num_sents'] += text_analysis['sentences']['num_sents']
		departments[lecture_dept]['sentences']['num_qmarks'] += text_analysis['sentences']['num_qmarks']
		departments[lecture_dept]['audience_participation']['num_audience_participations'] += text_analysis['audience_participation']['num_audience_participations']

	for dept in departments:
		if departments[dept]['total_duration'] > 0:
			departments[dept]['words']['wpm'] = (departments[dept]['words']['num_words'] / departments[dept]['total_duration']) * 60
			departments[dept]['sentences']['qmarks_per_hour'] = (departments[dept]['sentences']['num_qmarks'] / departments[dept]['total_duration']) * 3600
			departments[dept]['audience_participation']['apr'] = (departments[dept]['audience_participation']['num_audience_participations'] / departments[dept]['total_duration']) * 3600
		else:
			departments[dept]['words']['wpm'] = 0
			departments[dept]['sentences']['qmarks_per_hour'] = 0
			departments[dept]['audience_participation']['apr'] = 0

		if departments[dept]['words']['num_words'] > 0:
			departments[dept]['words']['avg_word_length'] = departments[dept]['total_chars'] / departments[dept]['words']['num_words']
			departments[dept]['words']['common_word_ratio'] = departments[dept]['words']['num_common_words'] / departments[dept]['words']['num_words']
		else:
			departments[dept]['words']['avg_word_length'] = 0
			departments[dept]['words']['common_word_ratio'] = 0

		if departments[dept]['sentences']['num_sents'] > 0:
			departments[dept]['sentences']['avg_words_per_sent'] = departments[dept]['words']['num_words'] / departments[dept]['sentences']['num_sents']
		else:
			departments[dept]['sentences']['avg_words_per_sent'] = 0

	with open(out_path, 'w') as departments_file:
		departments_file.write(json.dumps(departments, indent=4))

def change_courses_to_contain_lecture_ids(out_path='data/courses.json'):
	with open('data/courses.json', 'r') as courses_file:
		courses = json.loads(courses_file.read())

	with open('data/lectures.json', 'r') as lectures_file:
		lectures = json.loads(lectures_file.read())

	lecture_ids_of_courses = {}
	for course_code in courses.keys():
		lecture_ids_of_courses[course_code] = []

	for lecture_id in lectures.keys():
		course_code = lectures[lecture_id]['course_code']
		lecture_ids_of_courses[course_code].append(lecture_id)

	for course_code in courses.keys():
		courses[course_code]['course_lectures'] = lecture_ids_of_courses[course_code]

	with open('data/courses.json', 'w') as courses_file:
		courses_file.write(json.dumps(courses, indent=4))

def generate_ranked_words(in_path='data/unigram_freq.csv', out_path='data/ranked_words.json'):
	word_freqs = open(in_path, 'r')
	word_freqs.readline()
	ranks = {}

	next_line = word_freqs.readline().strip()
	index = 1
	while next_line:
		word, appearances = next_line.split(',')
		ranks[word] = index
		next_line = word_freqs.readline().strip()
		index += 1

	with open(out_path, 'w') as out_file:
		out_file.write(json.dumps(ranks, indent=4))

def get_names_from_text(instructors):
	for index, instructor in enumerate(instructors):
		instructor = instructor.strip()

		if instructor[:5] == 'Prof.':
			instructor = instructor[5:]
		if instructor[:3] == 'Dr.':
			instructor = instructor[3:]
		if instructor[:4] == 'Col.':
			instructor = instructor[4:]

		instructor = instructor.strip()
		names = instructor.split(' ')
		fname_abbreviated = ('.' in names[0])

		if not fname_abbreviated:
			names = [i for i in names if i[-1] != '.']
			instructor = ' '.join(names)

		instructors[index] = instructor

	return [i.strip() for i in instructors]

def get_names_from_description(soup):
	try:
		video_page_div = soup.findAll('div', {'class': 'video-page'})[0]
		description_div = video_page_div.findChildren('div', {'class': 'description'})[0]
	except IndexError:
		return []

	if not 'instructor' in str(description_div).lower():
		return False

	instructors = description_div.findChildren()[-1].text

	for child in description_div.findChildren(recursive=False):
		if child.findAll('strong') and ('instructor' in str(child).lower()):
			instructors = child.text.strip()

	instructors = instructors.replace('Â ', ' ')
	instructors = instructors.replace(' - ', ' ')
	instructors = instructors.replace(' ‑ ', ' ')
	instructors = instructors.replace('â\x80\x91 ', ' ')
	instructors = instructors.replace('guest lecturer', '').replace('Guest lecturer', '').replace('Guest Lecturer', '')
	first_space = instructors.index(' ')
	instructors = instructors[first_space+1:]
	instructors = instructors.replace(' and ', ', ')
	instructors = instructors.replace('&', ', ')
	instructors = instructors.replace(';', ', ')
	instructors = instructors.split(',')
	instructors = get_names_from_text(instructors)

	return [i.strip() for i in instructors if i]

def get_names_from_sidebar(soup):
	course_info_sections = soup.findAll('div', {'class': 'panel-course-info-title'})
	instructor_section = None

	for section in course_info_sections:
		if 'instructor' in section.text.lower():
			instructor_section = section.parent

	instructor_tags = instructor_section.findChildren()[1].findChildren()[0].findChildren()
	instructor_names = []

	for instructor in instructor_tags:
		instructor_names.append(instructor.text.strip())

	instructor_names = instructor_names[::2]
	if '' in instructor_names:
		instructor_names = instructor_names[3:-1]

	instructor_names = get_names_from_text(instructor_names)
	return instructor_names

def get_captions(soup):
	video_section = soup.findAll('track', {'kind': 'captions'})
	captions_url = ''

	if video_section:
		captions_url = 'https://ocw.mit.edu' + video_section[0]['src']

	return captions_url

def get_lecture_info(html):
	soup = BeautifulSoup(html, 'html.parser')

	captions_url = get_captions(soup)

	try:
		instructor_names = get_names_from_description(soup)
	except:
		instructor_names = get_names_from_sidebar(soup)

	if not instructor_names:
		instructor_names = get_names_from_sidebar(soup)		

	return [instructor_names, captions_url]

def is_good_url(url):
	try:
		r = requests.get(url)
		return r.ok
	except:
		return False

def get_lecture_urls(course_url):
	html = requests.get(course_url).text
	soup = BeautifulSoup(html, 'html.parser')
	side_menu = soup.select(
		'.col-2.course-home-grid.large-and-above-only'
	)[0].findChildren('a', {'class': 'nav-link'})

	lectures_url = ''
	for section in side_menu:
		title = section.text
		if ("video lecture" in title.lower()) or ("lecture video" in title.lower()):
			lectures_url = 'https://ocw.mit.edu' + section['href']

	print(lectures_url)

	if not lectures_url:
		return []
	try:
		r = requests.get(lectures_url)
		if not r.ok:
			return []
	except:
		return []

	html = BeautifulSoup(r.text, 'html.parser')
	lectures = html.findAll('a', {'class': 'video-link'})
	lecture_urls = []

	for lecture in lectures:
		lecture_url = 'https://ocw.mit.edu' + lecture['href']
		lecture_urls.append(lecture_url)

	return lecture_urls

def get_department_from_course_code(course_code):
	course_code_prefix = course_code.split('.')[0]
	if course_code_prefix in department_ids:
		return department_ids[course_code_prefix]
	else:
		return 'N/A'

def get_rhetorical_style_from_prof_name():
	pass

def get_rhetorical_style_from_lecture_id(lecture_id):
	try:
		captions = webvtt.read(f'data/transcripts/{lecture_id}.vtt')
	except FileNotFoundError:
		return {}

	lines = []
	for line in captions:
		end_time = line.end
		line = str(line.text).replace('\n', ' ')
		lines.append(line)

	full_text = ' '.join(lines)
	words = word_tokenize(full_text)
	sents = sent_tokenize(full_text)

	length = datetime.strptime(end_time, '%H:%M:%S.%f')
	reference_point = datetime(1900, 1, 1, 0, 0, 0)

	num_seconds = (length - reference_point).total_seconds()
	num_common_words = get_num_common_words(words)
	num_words = len(words)
	num_sents = len(sents)
	num_chars = sum([len(word) for word in words])
	num_audience_participations = full_text.count('AUDIENCE:')
	num_qmarks = full_text.count('?')

	if num_sents > 0:
		avg_words_per_sent = num_words / num_sents
	else:
		avg_words_per_sent = 0
	
	if num_words > 0:
		common_word_ratio = num_common_words / num_words
		avg_word_length = num_chars / num_words
	else:
		common_word_ratio = 0
		avg_word_length = 0

	if num_seconds > 0:
		num_wpm = (num_words / num_seconds) * 60
		apr = num_audience_participations / num_seconds * 3600
		qmarks_per_hour = (num_qmarks / num_seconds) * 3600
	else:
		num_wpm = 0
		apr = 0
		qmarks_per_hour = 0

	return {
		'duration': num_seconds,
		'num_chars': num_chars,
		'words': {
			'wpm': num_wpm,
			'num_words': num_words,
			'avg_word_length': avg_word_length,
			'num_common_words': num_common_words,
			'common_word_ratio': common_word_ratio
		},
		'sentences': {
			'num_sents': num_sents,
			'avg_words_per_sent': avg_words_per_sent,
			'num_qmarks': num_qmarks,
			'qmarks_per_hour': qmarks_per_hour
		},
		'audience_participation': {
			'apr': apr,
			'num_audience_participations': num_audience_participations
		}
	}


def is_real_word(word):
	word = word.strip('.,!?"%$')
	word = word.replace('-', '')

	if not word.isalpha():
		return False

	if len(word) == 1:
		return (word == 'a') or (word == 'i')

	return True

def word_tokenize(full_text):
	words = full_text.split(' ')
	words = [word for word in words if is_real_word(word)]

	return words

def get_num_common_words(words):
	num_common_words = 0

	for word in words:
		word = word.strip('.,!?"%$')
		word = word.replace('-', '')
		word = word.lower()

		if not word in ranked_words:
			continue

		if ranked_words[word] <= 500:
			num_common_words += 1

	return num_common_words

if __name__ == '__main__':
	print("-"*50 + "\nPART 1/5: Getting URLs of all lectures (creating courses.json)\n" + "-"*50)
	generate_course_catalog()
	print("-"*50 + "\nPART 2/5: Getting information about all lectures from aforementioned urls and downloading transcripts (creating lectures.json and transcripts folder)\n" + "-"*50)
	generate_lecture_ids()
	print("-"*50 + "\nPART 3/5: Generating profiles of professors from previously scraped data (creating professors.json)\n" + "-"*50)
	generate_professors()
	print("-"*50 + "\nPART 4/5: Generating profiles of departments from previously scraped data (creating departments.json)\n" + "-"*50)
	generate_departments()
	print("-"*50 + "\nPART 5/5: Modifying coures.json to store lecture ids of lectures rather than URLs to lectures (modifying courses.json)\n" + "-"*50)
	change_courses_to_contain_lecture_ids()