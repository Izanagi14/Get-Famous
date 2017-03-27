from tweepy import OAuthHandler
from tweepy import API
from auth import TwitterAuth
import datetime


def twitterDateToDaysFromNow(twitterString):
    twitterDate = datetime.strptime(twitterString, '%a %b %d %H:%M:%S +0000 %Y')
    return (datetime.now() - twitterDate).days

def __getFeatures(tweet, ids, featuresList, viralityList, keepTweetWithoutHashtags):
    features = []
    if 'retweeted_status' in tweet:
        user = tweet['retweeted_status']['user']
    else:
        user = tweet['user']

    features.append(max(user['followers_count'], 0))
    features.append(max(user['friends_count'], 0))
    features.append(max(user['listed_count'], 0))
    features.append(max(user['statuses_count'], 0))
    features.append(max(user['favourites_count'], 0))

    features.append(twitterDateToDaysFromNow(user['created_at']))
    if user['verified']:
        features.append(1)
    else:
        features.append(0)

    if 'hashtags' in tweet['entities']:
        features.append(len(tweet['entities']['hashtags']))
        if len(tweet['entities']['hashtags']) == 0 and keepTweetWithoutHashtags == False:
            return
    else:
        if keepTweetWithoutHashtags == False:
            return
        features.append(0)

    if 'media' in tweet['entities']:
        features.append(len(tweet['entities']['media']))
    else:
        features.append(0)

    if 'user_mentions' in tweet['entities']:
        features.append(len(tweet['entities']['user_mentions']))
    else:
        features.append(0)

    if 'urls' in tweet['entities']:
        features.append(len(tweet['entities']['urls']))
    else:
        features.append(0)

    if 'text' in tweet:
        features.append(min(len(tweet['text']), 140))
    else:
        features.append(0)

    retweet_count = tweet['retweet_count']
    if retweet_count > 3000000:
        return

    virality = []
    virality.append(max(retweet_count, 0))
    virality.append(max(tweet['favorite_count'], 0))
    virality.append(max(tweet['retweet_count'], 0) + max(tweet['favorite_count'], 0))

    ids.append(tweet['id'])
    featuresList.append(features)
    viralityList.append(virality)


class TwitterSearch:
    tweets={}
    tweetIDs = []
    FEATURE_LABEL = ['followers_count', 'friends_count', 'listed_count', 'statuses_count',
                     'favourites_count', 'days_from_account_creation', 'verified', 'hashtags', 'media',
                     'user_mentions', 'urls', 'text_len']
    VIRALITY_LABEL = ['retweet_count']

    HDF5_FILEPATH = "features2.hdf5"

    #TWITTER_DATABASE = "Twitter"
    #TWEETS_TABLE = "dups_removed5"

    @staticmethod
    # perform authentication
    def __authenticate():
        auth = OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
        auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)
        return API(auth)

    @staticmethod
    # search for given query
    def querySearch(query, maxAge=24, requests=180, lang="en"):

        api = TwitterSearch.__authenticate()
        requests = min(requests, 180)
        now = datetime.datetime.now()
        earlier = now - datetime.timedelta(hours = maxAge)
        oldestID = 0
        for i in range(0,requests):
            if oldestID == 0:
                TwitterSearch.tweets = api.search(q=query, count = 100, lang=lang, result_type="recent")
            else:
                TwitterSearch.tweets = api.search(q=query, count = 100, lang=lang, result_type="recent", max_id = oldestID-1)
            #if len(tweets) == 0:
                #return TwitterSearch.tweetIDs
            oldestID = TwitterSearch.tweets[len(TwitterSearch.tweets)-1].id
            #print TwitterSearch.tweets
            for tweet in TwitterSearch.tweets:
                print tweet.user.name

                # for kk in tweet.entities['user_mentions']:
                #     print kk['screen_name']






def main():
    ts = TwitterSearch()
    ts.querySearch("India")
    featuresList =[]
    viralityList = []
    __getFeatures(ts.tweets,ts.tweetIDs,featuresList,viralityList,False)

if __name__ == "__main__":
    main()
