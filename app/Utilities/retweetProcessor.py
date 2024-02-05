import Utilities.connectionMethods
import json

cur = Utilities.connectionMethods.getmySQLPointer()

createTable = \
    "CREATE TABLE RETWEETS(TweetID varchar(100), RTweetID varchar(100), RTHandle varchar(255), Retweeter varchar(100), RTTime varchar(100))"

cur.execute(createTable)

cur.fetchall()
commitCounter = 0
with open("../corona-out-3", "r", encoding='cp437', errors="ignore") as file:
    for line in file:
        try:
            data = json.loads(line)
            if(data['text'].startswith("RT")):
                cur.execute("INSERT INTO RETWEETS (TweetID, RTweetID, Retweeter, RTTime, RTHandle) VALUES ('%s', '%s', '%s', '%s', '%s')" % (data["retweeted_status"]["id_str"], data["id_str"], data["user"]["id_str"], data["created_at"], data["user"]['screen_name'].replace("\"", "'")))
            commitCounter += 1
            if (commitCounter >= 1000):
                Utilities.connectionMethods.commit()
                commitCounter = 0

        except:
            continue
Utilities.connectionMethods.commit()