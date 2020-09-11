from azure.cosmos import CosmosClient
from datetime import date
import os

url = os.environ['ACCOUNT_URI']
key = os.environ['ACCOUNT_KEY']
client = CosmosClient(url, credential=key)
database_name = "getyourubccourse"
database = client.get_database_client(database_name)
container_name = "Premium"
container = database.get_container_client(container_name)

# Iterates through all database entries and returns a list of premium users
# @returns {List <Item>} user : a premium user
def getAllUsers():
	requests = []
	for item in container.query_items(query='SELECT * FROM c', enable_cross_partition_query=True):
		requests.append([item["email"], item["dateAdded"]])
	return requests

# Returns true if the user has premium status
# @params {string} email: user's email that is also used as the partition key for this container
def isPremiumUser(email):
	query = "SELECT * FROM c WHERE c.email = @email"
	params = [
		{"name":"@email" , "value": email}
	]
	return len(list(container.query_items(query=query, parameters=params, enable_cross_partition_query=True))) > 0


# Removes a premium account from the list
# @params {string} email: user's email that is also used as the partition key for this container
def deletePremiumUser(email):
	query = "SELECT * FROM c WHERE c.email = @email"
	params = [
		{"name":"@email" , "value": email}
	]
	for item in container.query_items(query=query, parameters=params, enable_cross_partition_query=True):
		container.delete_item(item["id"], email)


# Adds a premium account to the list with the current date
# @params {string} email: user's email that is also used as the partition key for this container
def addPremiumUser(email):
	container.upsert_item(
        {
    		"email": email,
    		"dateAdded": str(date.today())
        }
    )
