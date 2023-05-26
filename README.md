# Professor-o-meter by goobergang

Conducting data analysis on MIT OpenCourseWare video lectures based on professors’ speech patterns, such as speed, common words, and student participation.

## Roster with roles
### Ziying Jian (PM)
- Integrating Foundations
- Building HTML pages
- Routing linkages in Javascript
- Assist with search bar

### Joshua Liu
- Constructing Flask app; template rendering
- Assisting in the creation of HTML templates
- Database manipulation

### Gabriel Thompson
- Database population
- Database creation
- Javascript 

### Jun Hong Wang
- Frontend
- Javascript
- Search bar

## Description of website
Presenting data analysis on MIT OpenCourseWare video lectures based on professors' and departments' speech patterns, such as verbosity, sentiment, speed, and student interactivity.

## Launch Codes
### How to clone/install
Clone this repo.
```
$ git clone git@github.com:zeeyingg/goobergang.git
```
Find your way into the repo.

```
$ cd goobergang/
```
Install required packages
```
$ pip install -r requirements.txt
```
### How to run
Enter the ```app``` directory
```
$ cd app
```
Paste the following line into your command prompt
```
python3 app/__init__.py
```
Enjoy Professor-o-meter in your local host address

### Data
#### Description
We collected our data by building an HTML scraper (```parse.py```). This tool both collated and performed calculations on our data, before storing them inside JSON files. Using the HTML scraper, we were also able to pull transcripts from the website with their timestamps. You can view all the source data on Kaggle. For a more concise view of all our calculations, you can view the Google Sheet.

#### Source
[MIT OpenCourseWare](https://ocw.mit.edu/)
[Google Sheet](https://docs.google.com/spreadsheets/d/1Bj-pP8pc98Gsd1SwsuEcpuDSyg7dbMeUnvXvPgjXR-Y/edit?usp=sharing)

