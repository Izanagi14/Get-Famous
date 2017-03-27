from datetime import datetime
import pymongo
import h5py

class FeatureExtractor23:
    FEATURE_LABEL = ['followers_count', 'friends_count', 'listed_count', 'statuses_count',
        'favourites_count', 'days_from_account_creation', 'verified', 'hashtags', 'media',
        'user_mentions', 'urls', 'text_len']
    VIRALITY_LABEL = ['retweet_count']


    HDF5_FILEPATH = "features2.hdf5"

    TWITTER_DATABASE = "Twitter"
    TWEETS_TABLE = "dups_removed5"
    @staticmethod
    def __twitterDateToDaysFromNow(twitterString):
        twitterDate = datetime.strptime(twitterString, '%a %b %d %H:%M:%S +0000 %Y')
        return (datetime.now() - twitterDate).days
    @staticmethod
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
        features.append(FeatureExtractor23.__twitterDateToDaysFromNow(user['created_at']))
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







