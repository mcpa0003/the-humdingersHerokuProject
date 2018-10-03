import os
import pandas as pd
import tweepy
import numpy as np
import time
import spacy
import en_core_web_sm
#import matplotlib
import matplotlib
matplotlib.use("Agg")
from datetime import datetime

#matplotlib.use("Agg")
# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
# Get config variable from environment variables
consumer_key = os.environ.get("consumer_key")
consumer_secret = os.environ.get("consumer_secret")
access_token = os.environ.get("access_token")
access_token_secret = os.environ.get("access_token_secret")

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

nlp = en_core_web_sm.load()

def update_twitter():


    # Create dictionary to hold text and label entities
    #changing something to push.
    tweet_dict = {"text": [], "label": []}

    mentions = api.search(q="@MichaelMcPart10 Analyze:")
    print(mentions)
    words = []
    try:

        command = mentions["statuses"][0]["text"]
        words = command.split("Analyze:")
        target_account = words[1].strip()
        print(f"analysis for target_account: {target_account}")
        user_tweets = api.user_timeline(target_account, page=1)
        
        sentiments = []

        # Loop through tweets
        for tweet in user_tweets:

            #doc = nlp(tweet["text"])

            if not doc.ents:
                print("No entities to visualize")
                print("----------------------------")
            else:
                # Print the entities for each doc
                for ent in doc.ents:
                    # Store entities in dictionary
                    tweet_dict["text"].append(ent.text)
                    tweet_dict["label"].append(ent.label_)
                                # Run Vader Analysis on each tweet
                    results = analyzer.polarity_scores(tweet["text"])
                    compound = results["compound"]
                    pos = results["pos"]
                    neu = results["neu"]
                    neg = results["neg"]

        tweet_df = pd.DataFrame(tweet_dict)
        tweet_df.head()

        label_frequency = tweet_df.groupby(["label"]).count()
        
        # Get Tweet ID, subtract 1, and assign to oldest_tweet
       ########### oldest_tweet = tweet['id'] - 1
        
        # Add sentiments for each tweet into a list
        sentiments.append({"Date": tweet["created_at"], 
                           "Compound": compound,
                           "Positive": pos,
                           "Negative": neu,
                           "Neutral": neg,
                           "Tweets Ago": counter})
                                 
                # Convert sentiments to DataFrame
        sentiments_pd = pd.DataFrame.from_dict(sentiments)
        sentiments_pd.head()
    # Create plot
        plt.figure(figsize=(6, 4), dpi=300)
        x_vals = sentiments_pd["Tweets Ago"]
        y_vals = sentiments_pd["Compound"]
        plt.plot(x_vals,
                 y_vals, marker="o", linewidth=0.3,
                 alpha=0.8)
#plt.figure(figsize=(6, 4), dpi=300)

# # Incorporate the other graph properties
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M")
        plt.title(f"Sentiment Analysis of Tweets ({now}) for {target_user}")
        plt.xlim([x_vals.max(),x_vals.min()]) #Bonus
        plt.ylabel("Tweet Polarity")
        plt.xlabel("Tweets Ago")
        plt.figure(figsize=(6, 4), dpi=300)
        plt.savefig("plot.png")
        api.update_with_media(
                "plot.png", "Vader Sentiment Analysis for " + target_account)


    # Grab Self Tweets
 #   tweets = api.user_timeline()

    except Exception:
        raise

    tweets = api.user_timeline()

    repeat = False

    for tweet in tweets:
        if target_account in tweet["text"]:
            repeat = True
            print("Sorry. Repeat detected!")

        else:
            continue


# Have the Twitter bot update once a day for a week
    days = 0
    while days < 7:
        print(f"This is just daily Tweet # {days} to check-in. Have a nice day!")

    # Update the twitter
        update_twitter()

    # Wait a day
        time.sleep(300)

    # Update day counter
        days += 1
    

