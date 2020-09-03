from bs4 import BeautifulSoup
import requests


# Takes in course information and returns the parse tree for the course schedule page HTML from courses.students.ubc.ca
# @params {string} dept : department of the course (eg. CPSC)
# @params {string} course : course number (eg. 201)
# @params {string} section : section number (eg. 001)
# @returns {soup} soup: parse tree for the HTML
def createHtmlSoup(dept, course, section):
	page = requests.get("https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=" 
		+ dept + "&course=" + course + "&section=" + section)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup


# Returns the number of total seats remaining in the course
# @params {soup} soup: parse tree for the HTML
# @returns {integer} totalSeatsRemaining : the number of total seats remaining in the course
def findTotalSeatsRemaining(soup):
	tdtags = soup.find_all("td")
	for i in range(0,len(tdtags)-1):
		if (tdtags[i].get_text() == "Total Seats Remaining:"):
			return int(tdtags[i+1].get_text())


# Returns whether or not the course is valid based on the soup parse tree
# @params {string} dept : department of the course (eg. CPSC)
# @params {string} course : course number (eg. 201)
# @params {string} section : section number (eg. 001)
# @returns {boolean} if the course is valid
def isCourseValid(dept, course, section):
	soup = createHtmlSoup(dept,course,section)
	return not "no longer offered" in soup.find_all("div", class_="content expand")[0].get_text()



# Returns whether or not there are greater than 0 total seats remaining in a course
# @params {string} dept : department of the course (eg. CPSC)
# @params {string} course : course number (eg. 201)
# @params {string} section : section number (eg. 001)
# @returns {boolean} if there is a course seat open
def isCourseSeatOpen(dept, course, section):
	soup = createHtmlSoup(dept,course,section)
	return findTotalSeatsRemaining(soup) > 0










