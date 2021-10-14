from flask import Flask
from flask import render_template
from flask import request
from .models import db, User, Tweet
from .predict import predict_user
from .twitter import wordto_vec, add_or_update_user
import os
import tweepy
import spacy
import re




app_dir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///{}".format(os.path.join(app_dir, "twitoff2.sqlite3"))

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = database
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)


    # Create tables
    with app.app_context():
        db.create_all()

    @app.route("/", methods =['GET', 'POST'])
    def main(name = None):
        name = request.form.get('user_name')
        if name:
            add_or_update_user(name)
    
        # TWITTER_API_KEY = "Bhcz6Og6MG7Yw4hL6kxX9f50L"
        # TWITTER_API_KEY_SECRET = "34Oew61N9gnd9LHCEHSyDnG8QHbK9FSgO2ylFTr8mXMpqfDySA"
        # auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
        # twitter = tweepy.API(auth)
        # twitter_user = twitter.get_user(screen_name = "nasa")
        # print(nasa.screen_name)
        # twitteruser_db = User(id=twitter_user.id, name = twitter_user.screen_name)
        # db.session.add(twitteruser_db)
        # db.session.commit()




        



        # if name:
        #     user = User(name=name)
        #     db.session.add(user)
            # db.session.commit()
        
        users = User.query.all()

        # twits = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode="Extended")
        # for twit in twits:
        #     tweet_vect = wordto_vec(twit.text)
        #     db_tweet = Tweet(id=twit.id,tweet =twit.text, tweet_vect=tweet_vect )
        # #     twitteruser_db.tweets.append(db_tweet)
        #     db.session.add(db_tweet)
            # db.session.commit()




        

        # tweet = request.form.get('tweet')

        # userid = request.form.get('userid')

        # if (tweet and userid):
        #     vectors= wordto_vec(tweet)
        #     userid = int(userid)
        #     tweet = Tweet(tweet =tweet, user_id = userid, tweet_vect =vectors)
            
        #     db.session.add(tweet)
        #     db.session.commit()

    
        tweets = Tweet.query.all()
        return render_template('base.html', users=users, tweets =tweets)
    @app.route('/iris')
    def iris():    
        from sklearn.datasets import load_iris
        from sklearn.linear_model import LogisticRegression
        X, y = load_iris(return_X_y=True)
        clf = LogisticRegression(random_state=0, solver='lbfgs',
                            multi_class='multinomial').fit(X, y)

        return str(clf.predict(X[:2, :]))
    # @app.route("/about")
    # def about():
    #     return "<p>collrestWorld!</p>"

    @app.route('/compare', methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values["user1"]])

        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            # prediction returns a 0 or 1
            prediction = predict_user(
                user0, user1, request.values["tweet_text"])
            message = "'{}' is more likely to be said by {} than {}!".format(
                request.values["tweet_text"],
                user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template('prediction.html', title="Prediction", message=message)

    return app
