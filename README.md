# Get-Famous

## Details ##
``` 
  1) The Project is about how the tweets get retweeted over time.
  2) Factors that affect a tweet getting retweeted(considering retweeted as virality of tweet) more.
  3) Analysing the factors to be used in the tweet to increase the virality of the tweet.
  4) Using machine learning alogorithms to see and predict the virality of the tweet.
```

### Implementation Details ###
``` 
  1) Out of many features available from the  tweet we have selected few:
       [ 'followers_count', 'friends_count', 'listed_count', 'statuses_count',
         'favourites_count', 'days_from_account_creation', 'verified', 'hashtags', 'media',
         'user_mentions', 'urls', 'text_len']
  2) The tweets are then taken from the twitter stream api and the features mentioned above are
     extracted from it.
  3) For the prediction we have tried a few of them, classification and regression.
  4) For data modelling we used numpy.
  5) The results are in the screenshots.
```

### How it works ###
```
    1) The virality of the tweet depends on the user tweeting the tweet and the mentions in the tweet,
    the video or any media associated with it, further the tweets are also affected if there in the tweet,
    there is some words which are really popular.
    2) We take the top ten viral hastags from twitter on the basis of the retweet count returned from the api,
    and then train the model according to the features and the retweet count as the output,
    keeping features vs the retweet count.
    3) We then directly fed the model in the regression model to train.
    4) For test train split we have used 3:7 ratio.
    5) If the tweet contains any of the top ten hashtags or its viral according to the features, 
    we can predict how viral the tweet is going to be.
```
  
