from azure.cosmos import CosmosClient
from CourseRequest import CourseRequest
import os

url = os.environ['ACCOUNT_URI']
key = os.environ['ACCOUNT_KEY']
client = CosmosClient(url, credential=key)
database_name = "getyourubccourse"
database = client.get_database_client(database_name)
container_name = "CourseRequests"
container = database.get_container_client(container_name)


# Iterates through all database entries and returns requests as a CourseRequest
# @returns {List <CourseRequest>} courserequest : list of all course requests from users
def getAllRequests():
	requests = []
	for item in container.query_items(query='SELECT * FROM c', enable_cross_partition_query=True):
		requests.append(CourseRequest(item["dept"],item["course"],item["section"],item["email"]))
	print(requests)


getAllRequests()