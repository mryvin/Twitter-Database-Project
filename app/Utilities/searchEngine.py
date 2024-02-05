import pymongo
import pickle
import Utilities.connectionMethods
from datetime import datetime
from Utilities.cacheStack import LRUCache

try:
    QueryCache = pickle.load("cache.pickle")
except:
    QueryCache = LRUCache()

tweets = Utilities.connectionMethods.getTweetsDB()
mySQL = Utilities.connectionMethods.getmySQLPointer()


def formatTweet(tweet):
    mySQL.execute("SELECT Handle FROM mydatabase.USERS1 WHERE UID = %s" % str(tweet['user_ID']))
    UName = mySQL.fetchall()[0][0]
    date_obj = datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S %z %Y')
    text = "Tweet from @" + UName + " on " + date_obj.strftime("%B %d, %Y").replace(" 0", " ") + ":\n\t"
    text += tweet["text"]
    text += "\n\t(" + str(tweet["favorite_count"]) + " Likes, " + str(tweet["reply_count"]) + " Replies, " + str(
        tweet["retweet_count"]) + " Retweets)"
    return text

def getReTweeters(postID):
    sqlQuery = "SELECT RTweetID, Retweeter, RTTime, RTHandle FROM mydatabase.retweets WHERE TweetID = " + str(postID)
    mySQL.execute(sqlQuery)
    return mySQL.fetchall()

def getUserProfile(userID):
    sqlQuery = "SELECT FName, Handle, FollowerCount, Verified, UserBio, YearJoined FROM mydatabase.users1 WHERE UID = " + str(
        userID)

    mySQL.execute(sqlQuery)
    results = mySQL.fetchall()
    UName, Handle, Followers, Verified, Bio, Joined = results[0]
    profile = "USER PROFILE FOR @" + Handle.strip() + ":"
    if (Verified == 1):
        profile += "\nVerified User"
    profile += "\n\tName:\t\t\t" + UName.strip()
    profile += "\n\tBio:\t\t\t" + Bio.strip()
    profile += "\n\tFollowers:\t\t" + str(Followers)
    profile += "\n\tMember Since:\t" + str(Joined)

    query = {"user": userID}
    tweets1 = tweets.find(query).sort("created_at", -1)
    for tweet in tweets1:
        profile += "\n" + formatTweet(tweet, UName)
    return profile
def text_user(text):
    cacheKey = ("text", "user", text)
    cacheResult = QueryCache.get(cacheKey)
    if cacheResult != -1:
        return cacheResult
    mySQL.execute("SELECT Handle FROM mydatabase.USERS1 WHERE LOWER(FName) LIKE '%%%s%%' ORDER BY InfluenceScore DESC" % text)
    users = mySQL.fetchall()
    results = []
    for result in users:
        results.append(result)
    QueryCache.put(cacheKey, cacheResult)
    return results

def user_user(handle):
    mySQL.execute("SELECT UID from mydatabase.users1 WHERE Handle LIKE '%s'" % handle)
    try:
        result = mySQL.fetchall()[0][0]
        return getUserProfile(result)
    except:
        return "No profile found with that handle. Try using the user lookup!"

def search_by_time(start, stop):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(stop, '%Y-%m-%d')

    start_date_formatted = start_date.strftime('%a %m %d %H:%M:%S +0000 %Y')
    end_date_formatted = end_date.strftime('%a %m %d %H:%M:%S +0000 %Y')

    query = {'created_at': {'$gte': start_date_formatted, '$lt': end_date_formatted}}
    matches = tweets.find(query).sort("retweet_count", -1)
    results = []
    for match in matches:
        results.append(match)
    return results

def text_tweets(text):
    cacheKey = ("text", "tweets", text)
    cacheResult = QueryCache.get(cacheKey)
    if cacheResult != -1:
        return cacheResult
    query = {"text": {"$regex": text}}
    sort_order = [("sumAB", pymongo.DESCENDING)]
    matches = tweets.aggregate([
        {"$match": query},
        {"$addFields": {"sumAB": {
            "$add": [{"$toDouble": "$reply_count"}, {"$toDouble": "$favorite_count"}, {"$toDouble": "$retweet_count"},
                     {"$toDouble": "$favorite_count"}]}}},
        {"$sort": {"sumAB": -1}}])
    results = []
    for match in matches:
        results.append(match)
    QueryCache.put(cacheKey, cacheResult)
    return results

def user_tweets(user):
    cacheKey = ("user", "tweets", user)
    cacheResult = QueryCache.get(cacheKey)
    if cacheResult != -1:
        return cacheResult
    mySQL.execute("SELECT UID from mydatabase.users1 WHERE Handle = '%s'" % user)
    uid = mySQL.fetchall()[0][0]
    query = {"user_ID": int(uid)}
    tweets1 = tweets.find(query).sort("created_at", -1)
    results = []
    for tweet in tweets1:
        results.append(tweet)
    QueryCache.put(cacheKey, cacheResult)
    return results

def hashtag_tweets(hashtag):
    cacheKey = ("hashtag", "tweets", hashtag)
    cacheResult = QueryCache.get(cacheKey)
    if cacheResult != -1:
        return cacheResult
    query = {"hashtags": {"$regex": hashtag}}
    sort_order = [("sumAB", pymongo.DESCENDING)]
    matches = tweets.aggregate([
        {"$match": query},
        {"$addFields": {"sumAB": {
            "$add": [{"$toDouble": "$reply_count"}, {"$toDouble": "$favorite_count"}, {"$toDouble": "$retweet_count"},
                     {"$toDouble": "$favorite_count"}]}}},
        {"$sort": {"sumAB": -1}}])

    results = []
    for match in matches:
        results.append(match)
    QueryCache.put(cacheKey, cacheResult)
    return results