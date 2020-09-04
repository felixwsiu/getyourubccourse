from azure.cosmos import CosmosClient
import os

url = os.environ['ACCOUNT_URI']
key = os.environ['ACCOUNT_KEY']
client = CosmosClient(url, credential=key)
database_name = "getyourubccourse"
database = client.get_database_client(database_name)
container_name = "Metrics"
container = database.get_container_client(container_name)

#The Metrics container only contains one object "metric" that will hold all values 
#Further metrics can be added to this object in the Metric Container
metric = container.read_item("metric","True")


# Returns the total amount of email notifications sent so far
def getTotalNotificationsSent():
	return metric["totalNotifications"]


# Adds one to the total notifications sent
def addTotalNotificationsSent():
	metric["totalNotifications"] = metric["totalNotifications"] + 1
	container.upsert_item(metric)

