import spacy
import tweepy
from .models import User, db, Tweet

TWITTER_API_KEY = "Bhcz6Og6MG7Yw4hL6kxX9f50L"
TWITTER_API_KEY_SECRET = "34Oew61N9gnd9LHCEHSyDnG8QHbK9FSgO2ylFTr8mXMpqfDySA"
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY,"TWITTER_API_KEY_SECRET")
TWITTER = tweepy.API(TWITTER_AUTH)

nlp = spacy.load("en_core_web_sm")
def wordto_vec(tweet):
    return nlp(tweet).vector


def add_or_update_user(username):
    """
    Gets twitter user and tweets from twitter DB
    Gets user by "username" parameter.
    """
    try:
        # gets back twitter user object
        twitter_user = TWITTER.get_user(screen_name = username)
        # Either updates or adds user to our DB
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, name=username)
        db.session.add(db_user)  # Add user if don't exist

        # Grabbing tweets from "twitter_user"
        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="extended",
            since_id=db_user.newest_tweet_id
        )

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # tweets is a list of tweet objects
        for tweet in tweets:
            # type(tweet) == object
            tweet_vector = wordto_vec(tweet.full_text)
            db_tweet = Tweet(
                id=tweet.id,
                text=tweet.full_text,
                vect=tweet_vector
            )
            db_user.tweets.append(db_tweet)
            db.session.add(db_tweet)

    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e

    else:
        db.session.commit()