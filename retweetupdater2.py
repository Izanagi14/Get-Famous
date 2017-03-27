from tweepy import OAuthHandler
from tweepy import API
from tweepy import TweepError
import tweepy
import time
import os
import numpy as np
from auth import TwitterAuth
import pymongo
class retweetUpdater:
	def __init__(self):
		auth=OAuthHandler(TwitterAuth.consumer_key,TwitterAuth.consumer_secret)
		auth.set_access_token(TwitterAuth.access_token,TwitterAuth.access_token_secret)
		self.api=API(auth)
	def statusLookup(self, tweetIDs, collection):
		for attempt in range(10):
			print 'line 17'
			try:
				tweets = self.api.statuses_lookup(tweetIDs)
				print 'tweets obtained'
				for tweet in tweets:
					tweetID=tweet.id
					print 'inside'+str(tweetID)
					doc=collection.find_one({'id':tweetID})
					doc['retweet_count']=tweet.retweet_count
					collection.replace_one({'id':tweetID},doc)
					print "retweet_count updated"
			except TweepError:
				print "tweepy error - try again"
	def updateCount(self,odbname,cname):
		try:
			print "Connecting to database"
			conn=pymongo.MongoClient()
			outputDB = conn[odbname]
			collection = outputDB[cname]
			apicalls=0
			tweetcount=0
			tweetids=[]
			docs=[]
			print("starting twitter.mp4 api calls")
			for doc in collection.find(no_cursor_timeout=True):
				tweetID=doc['id']
				print tweetID
				doc['retweet_count']=-1
				collection.replace_one({'id':tweetID},doc)
				tweetids.append(tweetID)
				docs.append(doc)
				tweetcount+=1
				print(tweetcount)
				if len(tweetids)==100:
					self.statusLookup(tweetids,collection)
					tweetids=[]
					docs=[]
					apicalls+=1 
				if apicalls==180:
					print "Sleep for 15 minutes - "+ time.strftime('%X') + "\n"
					time.sleep(15*60)
					apicalls = 0
			if len(tweetids)!=0:
				self.statusLookup(tweetids,collection)
				print "Progress: " + str(tweetcount)
			collection.delete_many({'retweet_count':-1})
		except pymongo.errors.ConnectionFailure as e:
			print "Could not connect to MongoDB:"+str(e)
def main():
	updater=retweetUpdater()
	outputDatabaseName = "Twitter"
	collectionName = "dups_removed5"
	updater.updateCount(outputDatabaseName,collectionName)
if __name__=='__main__':
	main()