import json
import Utilities.connectionMethods

temp = Utilities.connectionMethods.getTweetsDB()

with open("corona-out-3", "r") as f1:
    for line in f1:
        try:
            data = json.loads(line)
            if temp.find_one({"id": data['id']}) is not None:
                continue

            user = data['user']
            if ( data['text'].startswith('RT') ):

                if temp.find_one({"id": data["retweeted_status"]["id"]}) is None:

                    if 'retweeted_status.extended_tweet' in data:
                        tweet_details = {
                            'created_at': data["retweeted_status"]['created_at'],
                            'updated_at' : data['created_at'],
                            'id': data["retweeted_status"]['id'],
                            'text': data["retweeted_status"]['extended_tweet']['full_text'],
                            'in_reply_to_user_id': data["retweeted_status"]['in_reply_to_user_id'],
                            'in_reply_to_status_id': data["retweeted_status"]['in_reply_to_status_id'],
                            'user_ID': data["retweeted_status"]['user']['id'],
                            'quote_count': data["retweeted_status"]['quote_count'],
                            'reply_count': data["retweeted_status"]['reply_count'],
                            'retweet_count': data["retweeted_status"]['retweet_count'],
                            'favorite_count': data["retweeted_status"]['favorite_count'],
                            'hashtags': data["retweeted_status"]['entities']['hashtags'],
                            'language': data["retweeted_status"]['lang']
                        }
                    else:
                        tweet_details = {
                            'created_at': data["retweeted_status"]['created_at'],
                            'updated_at' : data['created_at'],
                            'id': data["retweeted_status"]['id'],
                            'text': data["retweeted_status"]['text'],
                            'in_reply_to_user_id': data["retweeted_status"]['in_reply_to_user_id'],
                            'in_reply_to_status_id': data["retweeted_status"]['in_reply_to_status_id'],
                            'user_ID': data["retweeted_status"]['user']['id'],
                            'quote_count': data["retweeted_status"]['quote_count'],
                            'reply_count': data["retweeted_status"]['reply_count'],
                            'retweet_count': data["retweeted_status"]['retweet_count'],
                            'favorite_count': data["retweeted_status"]['favorite_count'],
                            'hashtags': data["retweeted_status"]['entities']['hashtags'],
                            'language': data["retweeted_status"]['lang']
                        }

                    result = temp.insert_one(tweet_details)
                else:
                    if data["created_at"] > temp.find_one({"id": data["retweeted_status"]["id"]})['updated_at']:

                        result = temp.update_one({"id": data["retweeted_status"]["id"]}, {"$set": {"updated_at": data["created_at"]}})
                        temp.update_one({"id": data["retweeted_status"]["id"]}, {"$set": {"quote_count": data["retweeted_status"]["quote_count"]}})
                        temp.update_one({"id": data["retweeted_status"]["id"]}, {"$set": {"reply_count": data["retweeted_status"]["reply_count"]}})
                        temp.update_one({"id": data["retweeted_status"]["id"]}, {"$set": {"retweet_count": data["retweeted_status"]["retweet_count"]}})
                        temp.update_one({"id": data["retweeted_status"]["id"]}, {"$set": {"favorite_count": data["retweeted_status"]["favorite_count"]}})
            else:
                if temp.find_one({"id": data["id"]}) is None:
                    if 'extended_tweet' in data:
                        tweet_details = {
                            'created_at': data['created_at'],
                            'updated_at' : data['created_at'],
                            'id': data['id'],
                            'text': data['extended_tweet']['full_text'],
                            'in_reply_to_user_id': data['in_reply_to_user_id'],
                            'in_reply_to_status_id': data['in_reply_to_status_id'],
                            'user_ID': data['user']['id'],
                            'quote_count': data['quote_count'],
                            'reply_count': data['reply_count'],
                            'retweet_count': data['retweet_count'],
                            'favorite_count': data['favorite_count'],
                            'hashtags': data['entities']['hashtags'],
                            'language': data['lang']
                        }
                    else:
                        tweet_details = {
                            'created_at': data['created_at'],
                            'updated_at' : data['created_at'],
                            'id': data['id'],
                            'text': data['text'],
                            'in_reply_to_user_id': data['in_reply_to_user_id'],
                            'in_reply_to_status_id': data['in_reply_to_status_id'],
                            'user_ID': data['user']['id'],
                            'quote_count': data['quote_count'],
                            'reply_count': data['reply_count'],
                            'retweet_count': data['retweet_count'],
                            'favorite_count': data['favorite_count'],
                            'hashtags': data['entities']['hashtags'],
                            'language': data['lang']
                        }
                    result = temp.insert_one(tweet_details)

        except:
            continue