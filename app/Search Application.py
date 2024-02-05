import Utilities.searchEngine
from datetime import datetime

exit = -1

def clearSearch():
    inputType = -1
    outputType = -1
    dataSearch = -1
    dateStart = -1
    dateEnd = -1
    searchString = ""

def presentTweetResults(results):
    if len(results) == 0 or type(results) is None:
        print("No results found.")
        return
    if len(results) <= 10:
        i = 1
        for result in results:
            print("\n----------\nResult " + str(i) + ": ")
            print(Utilities.searchEngine.formatTweet(result))
            i += 1
        next = -1
        while next != 0:
            next = int(input("Would you like to follow up on a result (1), or finish this search (0)? "))
            if next == 0:
                return
            if next == 1:
                target = int(input("Which result number? ")) -1
                command = int(input("Would you like to see the user's profile (1) or view the post's retweets (2)? "))
                if command == 1:
                    print(Utilities.searchEngine.getUserProfile(results[target]["user_ID"]))
                    continue
                if command == 2:
                    for rt in Utilities.searchEngine.getReTweeters(results[target]["id"]):
                        date_str = rt[2]
                        date_obj = datetime.strptime(date_str, '%a %b %d %H:%M:%S %z %Y')
                        formatted_date = date_obj.strftime("%B %d, %Y").replace(" 0", " ")
                        print("Retweeted by:\t", rt[3], "\n\t\t  on:\t", formatted_date)

    if len(results) >= 10:
        start = 0
        stop = 10
        i = 1
        print(results[start:stop])
        for result in results[start:stop]:
            print("\n----------\nResult " + str(i) + ": ")
            print(Utilities.searchEngine.formatTweet(result))
            i += 1
        next = -1
        while next != 0:
            next = int(input("Would you like to see more results (1), follow up on a result (2), or finish this search (0)? "))
            if next == 0:
                return
            if next == 1:
                start += 10
                stop += 10
                for result1 in results[start:stop]:
                    print("\n----------\nResult " + str(i) + ": ")
                    print(Utilities.searchEngine.formatTweet(result1))
                    i += 1
            if next == 2:
                target = int(input("Which result number?" )) - 1
                command = int(input("Would you like to see the user's profile (1) or view the post's retweets (2)? "))
                if command == 1:
                    print(Utilities.searchEngine.getUserProfile(results[target]["user_ID"]))
                    continue
                if command == 2:
                    for rt in Utilities.searchEngine.getReTweeters(results[target]["id"]):
                        date_str = rt[2]
                        date_obj = datetime.strptime(date_str, '%a %b %d %H:%M:%S %z %Y')
                        formatted_date = date_obj.strftime("%B %d, %Y").replace(" 0", " ")
                        print("Retweeted by:\t", rt[3], "\n\t\t  on:\t", formatted_date)



def presentUserResults(results):
    return




print("\n\nWelcome to the search application.")
while exit != 0:
    clearSearch()
    outputType = int(input("\n\nWould you like to search for tweets (1), users (2), or exit the application (3)? "))
    if outputType == 1:
        inputType = int(input("Would you like to search for tweets by user (1), hashtag (2), phrase (3), or time range (4)?"))
        if inputType == 1:
            searchString = input("Please enter their twitter handle. ")
            presentTweetResults(Utilities.searchEngine.user_tweets(searchString))
            continue
        elif inputType == 2:
            searchString = str(input("Please enter a hashtag. "))
            presentTweetResults(Utilities.searchEngine.hashtag_tweets(searchString))
            continue
        elif inputType == 4:
            startDate = str(input("Please enter the start date in the YYYY-MM-DD format: "))
            endDate =  str(input("Please enter the end date in the YYYY-MM-DD format: "))
            presentTweetResults(Utilities.searchEngine.search_by_time(startDate, endDate))
        elif inputType == 3:
            searchString = str(input("Please enter your query. "))
            presentTweetResults(Utilities.searchEngine.text_tweets(searchString))
        else:
            print("Sorry, we are unable to process your request. Restarting your search. ")
            continue
    elif outputType == 2:
        inputType = int(input("Would you like to look up a user by their name (1) or see a user profile (2)? "))
        if inputType == 1:
            searchString = str(input("Please enter the user's name. "))
            for result in Utilities.searchEngine.text_user(searchString)[0:10]:
                print("Potential Match: @" + result[0])
            continue
        elif inputType == 2:
            searchString = str(input("Please enter the user's handle. "))
            print(Utilities.searchEngine.user_user(searchString))
            continue
        else:
            print("Sorry, we are unable to process your request. Restarting your search. ")
            continue
    elif outputType == 3:
        print("Sounds good. bye! ")
        exit = 0
        continue
