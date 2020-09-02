# A CourseRequest that is submitted from a user trying to get into a course
# Attributes:
# {string} dept : department of the course (eg. CPSC)
# {string} course : course number (eg. 201)
# {string} section : section number (eg. 001)
# {email} email : email of the user

class CourseRequest:

	def __init__(self, dept, course, section, email, dateAdded):
		self.dept = dept
		self.course = course
		self.section = section
		self.email = email
		self.dateAdded = dateAdded


