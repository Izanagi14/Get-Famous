import pymongo
#python script to remove duplicates tweet entries from tweets database
#dup_remove will accept database name and collection name and and index name which is to be made unique
#creates new collection remove _id from previously extracted document and create unique index value for index to be made unique
	
def dup_remove(dbname,cname,indexname):
	dup_count=0
	cont=0
	try:
		conn=pymongo.MongoClient()
		outputDB=conn[dbname]
		collection=outputDB[cname]
		newcollection=outputDB['dups_removed5']
		newcollection.create_index([('id',pymongo.ASCENDING)],unique=True)
		handler=collection.find()
		for i in handler:
			try:
				if '_id' in i:
					del i['_id']
				print("k")
				newcollection.insert(i)
			except pymongo.errors.DuplicateKeyError as e:
				print("duplicate base")
				dup_count=dup_count+1
				print(dup_count)
	except :
		print("unexpected error")
if __name__=='__main__':
	dup_remove('Twitter','Tweets','id')