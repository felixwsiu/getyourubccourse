from azure.cosmos import CosmosClient
from CourseRequest import CourseRequest
from datetime import date
import os

url = os.environ['ACCOUNT_URI']
key = os.environ['ACCOUNT_KEY']
client = CosmosClient(url, credential=key)
database_name = "getyourubccourse"
database = client.get_database_client(database_name)
container_name = "CourseRequests"
container = database.get_container_client(container_name)

# The number of free requests a user can have in our DB
maxfreerequests = 3


# Iterates through all database entries and returns requests as a CourseRequest
# @returns {List <CourseRequest>} courserequest : list of all course requests from users
def getAllRequests():
	requests = []
	for item in container.query_items(query='SELECT * FROM c', enable_cross_partition_query=True):
		requests.append(CourseRequest(item["dept"],item["course"],item["section"],item["email"],item["dateAdded"],item["id"],item["premium"]))
	return requests


# Returns a course request with the given id
# @params {string} id: the id of the course request
# @returns {CourseRequest or boolean} : course request from the db, returns false if the course could not be found
def getCourseRequest(id):
	for item in container.read_all_items():
		if item["id"] == id:
			return item
	return False


# Adds a course request to the database
# @params {string} dept : department of the course (eg. CPSC)
# @params {string} course : course number (eg. 201)
# @params {string} section : section number (eg. 001)
# @params {string} email: email to send the notification
def addRequest(dept, course, section, email,premium):
	container.upsert_item(
        {
            "dept": dept,
    		"course": course,
    		"section": section,
    		"email": email,
    		"dateAdded": str(date.today()),
    		"premium": premium
        }
    )

# Checks for a duplicate copy of a course request
# @params {string} dept : department of the course (eg. CPSC)
# @params {string} course : course number (eg. 201)
# @params {string} section : section number (eg. 001)
# @params {string} email: email to send the notification
# @returns {boolean} whether true if there isnt a duplicate request
def doesNotDuplicate(dept, course, section, email):
	query = "SELECT * FROM c WHERE c.email = @email AND c.dept = @dept AND c.course = @course AND c.section = @section"
	params = [
		{"name":"@email" , "value": email},
		{"name":"@dept" , "value": dept},
		{"name":"@course" , "value": course},
		{"name":"@section" , "value": section},
	]
	return len(list(container.query_items(query=query, parameters=params, enable_cross_partition_query=True))) <= 0



# Removes a course request from the database
# @params {string} id: unique id name for the representing request
# @params {string} email: user's email that is also used as the partition key for this container
def deleteRequest(id, email):
	container.delete_item(id, email)


# Returns whether a user has the max amount of requests in the database
# @params {string} email: users email
# @returns {boolean} true if the user has reached the maximum amount of requests (maxfreerequests)
def isMaxRequests(email):
	query = "SELECT * FROM c WHERE c.email = @email"
	params = [
		{"name":"@email" , "value": email}
	]
	count = 0
	for item in container.query_items(query=query, parameters=params, enable_cross_partition_query=True):
		count = count + 1
	return count >= maxfreerequests

# Turns on premium status on current requests for a given user
# @params {string} email : users email
def updateRequestsWithPremium(email):
	query = "SELECT * FROM c WHERE c.email = @email"
	params = [
		{"name":"@email" , "value": email}
	]
	for item in container.query_items(query=query, parameters=params, enable_cross_partition_query=True):
		item["premium"] = True
		container.upsert_item(item)

