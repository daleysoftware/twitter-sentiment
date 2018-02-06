import sys
import tweepy
import logging
import textblob


consumer_key = "<redacted>"
consumer_secret = "<redacted>"
access_key = "<redacted>"
access_secret = "<redacted>"


def fetch_tweets(username):
    logging.info("Authenticating with Twitter...")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    logging.info("Fetching tweets...")
    new_tweets = api.user_timeline(screen_name=username, count=200)
    all_tweets = new_tweets
    oldest = all_tweets[-1].id - 1
    page = 1
    while len(new_tweets) > 0:
        page += 1
        logging.info("Fetching page %s" % page)
        new_tweets = api.user_timeline(screen_name=username, count=200, max_id=oldest)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
    logging.info("Fetched %s tweets" % len(all_tweets))
    return all_tweets


def perform_sentiment_analysis(tweets):
    result = []
    for tweet in tweets:
        testimonial = textblob.TextBlob(tweet._json['text'])
        result.append(testimonial.sentiment.polarity)
    return result


def main(username):
    tweets = fetch_tweets(username)
    sentiment_analysis_result = perform_sentiment_analysis(tweets)

    if len(sentiment_analysis_result) == 0:
        print("No tweets found.")

    negative_count = 0
    positive_count = 0

    for sar in sentiment_analysis_result:
        if sar < 0:
            negative_count += 1
        else:
            positive_count += 1

    print("Tweets found: %s" % len(tweets))
    print("Positive: %s" % round((100 * positive_count / (len(tweets))), 1))
    print("Negative: %s" % round((100 * negative_count / (len(tweets))), 1))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        logging.basicConfig(level=logging.INFO)
        main(sys.argv[1])
    else:
        print("Usage: %s <username>" % sys.argv[0])
