from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json
import pymongo



class StdOutListener(StreamListener):

	def __init__(self, outputDatabaseName, collectionName):
		try:
			print "Connecting to database"
			conn=pymongo.MongoClient()
			outputDB = conn[outputDatabaseName]
			self.collection = outputDB[collectionName]
			self.counter = 0
		except pymongo.errors.ConnectionFailure, e:
			print "Could not connect to MongoDB: %s" % e 
	
	#This function gets called every time a new tweet is received on the stream
	def on_data(self, data):	
		#Convert the data to a json object (shouldn't do this in production; might slow down and miss tweets)
		datajson=json.loads(data)

		#Check the language
		if "lang" in datajson and datajson["lang"] == "en" and "text" in datajson:
			self.collection.insert(datajson)

			#See Twitter reference for what fields are included -- https://dev.twitter.com/docs/platform-objects/tweets
			text=datajson["text"].encode("utf-8") #The text of the tweet
			self.counter += 1
			print(str(self.counter) + " " +text) #Print it out

	def on_error(self, status):
		print("ERROR")
		print(status)

	def on_connect(self):
		print("You're connected to the streaming server.")

if __name__ == '__main__':
	try:
		# Database settings
		outputDatabaseName = "m_project1"
		collectionName = "newc4"

		#Create the listener
		# l = StdOutListener(outputDatabaseName, collectionName)
		# auth=OAuthHandler("xN4Gae4NeL91wPw8UbZLl29Yf","yRIwNJUKpmpkoQHMk9UwomQx2EcQVb3rz1C4PkNHhkpyCaMnA7")
		# auth.set_access_token("2359225466-cBTrmfcbtKRlrNlvufoHeiGtVnBYEF5PYyGR8Tf","bMI2vCSJoXRGDvIUA5CjBdUaufXvhxZVXiR3XSIeVQjwI")
        #
		# #Connect to the Twitter stream
		# stream = Stream(auth, l)
        #
		# #Terms to track
		# stream.filter(track=["india"])

	except KeyboardInterrupt:
		#User pressed ctrl+c -- get ready to exit the program
		pass
