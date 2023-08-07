import tweepy
import datetime
arr=[]

class getTweets:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.api = None

        # credentials
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def setAuth(self):
        try:
            self.auth = tweepy.OAuthHandler(
                self.consumer_key, self.consumer_secret)
            self.auth.set_access_token(
                self.access_token, self.access_token_secret)
            self.api = tweepy.API(
                self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            if self.api.verify_credentials():
                print('Authentication OK')
            else:
                print('Error occurred during authentication!')
        except tweepy.TwitterServerError as err:
            print('Error: {}'.format(err))

    def writeToFile(self, filename='tw.csv', query='#dataviz', count=100, lang='tr', since=None, until=None, items=1000):
        

        currentTime = datetime.datetime.today().strftime('%Y-%m-%d')
        previousTime = (datetime.datetime.today() -
                        datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        try:
            # print('Initializing...')
            ids = set()
            # csvFile = open(filename, 'a')
            # csvWriter = csv.writer(csvFile)
            
            for tweet in tweepy.Cursor(self.api.search,
                                       q=query,
                                       count=count,
                                       lang=lang,
                                       tweet_mode='extended',
                                       since=until if until else previousTime,
                                       until=since if since else currentTime).items(items):
                if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
                    if('"' not in tweet.full_text):
                        ids.add(tweet.id)
                        arr.append(tweet.full_text)
                        with open(filename, 'a') as file:
                            file.write(tweet.full_text+"\n")
        except Exception as err:
            print('Error: {}'.format(err))
        finally:
            print('Completed!')
            # csvFile.close()
    def twitterSearch(self, save_path,word):
        self.writeToFile(filename=save_path, query=word, count=100, lang='tr', items=1000)
