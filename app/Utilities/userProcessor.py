import Utilities.connectionMethods
import json

cur = Utilities.connectionMethods.getmySQLPointer()

createTable = \
    "CREATE TABLE USERS1( \
    UID varchar(50) NOT NULL PRIMARY KEY,   \
    FName varchar(255),              \
    Handle varchar(255),            \
    FollowerCount int,              \
    FriendCount int,                \
    LikesCount int,                 \
    TweetsCount int,                \
    Verified int,                  \
    InfluenceScore FLOAT(24),       \
    UserBio varchar(500),           \
    YearJoined int)"

cur.execute(createTable)

def stripQuotes(text):
    return text.replace("\'", "").replace("\"", "").replace("\\\'", "").replace("\\\"", "")


def UsertoMySQL(data):
    string = "SELECT COUNT(1) FROM mydatabase.USERS1 WHERE UID = %s" % data['id_str']
    cur.execute(string)
    if (cur.fetchall()[0][0] != 0):
        return
    UserID = stripQuotes(data['id_str']) if data['id_str'] is not None else ""
    Name = stripQuotes(data['name']) if data['name'] is not None else ""
    Handle = stripQuotes(data['screen_name']) if data['screen_name'] is not None else ""
    Bio = stripQuotes(data['description']) if data['description'] is not None else ""
    Verified = int(data['verified']) if data['verified'] is not None else 0
    Followers = data['followers_count'] if data['followers_count'] is not None else 0
    Friends = data['friends_count'] if data['friends_count'] is not None else 0
    Likes = data['favourites_count'] if data['favourites_count'] is not None else 0
    Tweets = data['statuses_count'] if data['screen_name'] is not None else 0
    JoinYear = int(data['created_at'][-4:]) if data['created_at'] is not None else 0000

    InfluenceScore = (3*int(Followers) + 2*int(Friends) + int(Tweets) + 0.5*int(Likes)) / 100
    if Verified:
        InfluenceScore = str(InfluenceScore * 1.25)

    sqlCMD = "INSERT INTO USERS1 (UID, FName, Handle, UserBio, FollowerCount, FriendCount, LikesCount, TweetsCount, Verified, InfluenceScore, YearJoined) VALUES (" \
             "'%s', '%s', '%s', '%s', " % (UserID, Name, Handle, Bio) + str((", ").join([str(Followers), str(Friends), str(Likes), str(Tweets), str(Verified), str(InfluenceScore), str(JoinYear)])) + ")"
    cur.execute(sqlCMD)

try:
    cur.fetchall()
except:
    pass

commitCounter = 0
inc = 0
with open("../corona-out-3", "r", encoding='cp437', errors="ignore") as file:
    for line in file:
        try:
            data = json.loads(line)
            try:
                UsertoMySQL(data['user'])
            except:
                inc += 1
            try:
                UsertoMySQL(data['retweeted_status']['user'])
            except:
                inc += 1
            try:
                UsertoMySQL(data['quoted_status']['user'])
            except:
                inc += 1
            commitCounter += 1
            if (commitCounter >= 1000):
                Utilities.connectionMethods.commit()
                commitCounter = 0
        except:
            continue
Utilities.connectionMethods.commit()