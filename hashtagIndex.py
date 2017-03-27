import pymongo
import pickle

class HashtagIndex:


    def __init__(self):
        self.index = {}
        try:
            self.loadIndex()
        except:
            print "Index file not found"
            self.generateIndex("Twitter", "dups_removed5")

    # Generate index and save to .pkl file
    def generateIndex(self, outputDatabaseName, collectionName):
        # type: (object, object) -> object
        try:
            conn=pymongo.MongoClient()
            outputDB = conn[outputDatabaseName]
            collection = outputDB[collectionName]
            print "Building inverted index from database..."
            # Query database for tweets containing hashtags
            test = collection.find({"entities.hashtags.text" : {"$exists": True}})
            for tweet in test:
                for hashtag in tweet["entities"]["hashtags"]:
                    if hashtag["text"] in self.index:
                        # Add tweet id to previously known hashtag
                        self.index[hashtag["text"]].append(tweet["id"])
                    else:
                        # Add tweet id to new hashtag
                        self.index[hashtag["text"]] = [tweet["id"]]
            # Save to .pkl file
            self.saveIndex()
        except:
            print "Could not generate index. Please check your database connection"

    # Save index to file
    def saveIndex(self):
        print "Saving hashtag index to file..."
        with open("hashtag_index"+ ".pkl", "wb") as f:
            pickle.dump(self.index, f, pickle.HIGHEST_PROTOCOL)
        print "Done saving the hashtag index"

    # Load index from file
    def loadIndex(self):
        print "Loading hashtag index..."
        with open("hashtag_index"+ ".pkl", "rb") as f:
            self.index = pickle.load(f)
        print "Done loading the hashtag index"

    # Returns a list of tweet ID's for the given hashtag
    def find(self, hashtag):
        if hashtag in self.index:
            return self.index[hashtag]
        else:
            return []

    def keys(self):
        # Return an array of hashtags
        return self.index.keys()

    def values(self):
        # Return an array of arrays of tweets ID
        return self.index.values()

    def items(self, sort=False, descending=False, min_values=0):
        
        # Return the index items, possibly sorted by ascending or descending (descending=True) order
        # Only the items having more than min_values values are returned
        if min_values > 1:
            result = [(k,v) for (k,v) in self.index.items() if len(v) >= min_values]
        else:
            result = self.index.items()

        if sort:
            result = sorted(result, key=lambda (v): len(v), reverse=descending)

        return result

if __name__ == "__main__":
    hashtagIndex = HashtagIndex()
    print hashtagIndex.index
    print hashtagIndex.find("no more") # Should print [592958600357793793L]
    print len(hashtagIndex.find('One ')) # Should print 105
