import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime


def add_a_day(date):
    """
    This function will add a day to the date
    :param date: The date to add a day to
    :return: The date with a day added
    """
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date = date + datetime.timedelta(days=1)
    date = date.strftime('%Y-%m-%d')
    return date



def get_tweets(search_term, start_date, end_date,number_of_tweets):

    """
    This function will return a list of tweets that match the search term
    :param search_term: The term to search for
    :param start_date: The start date of the search
    :param end_date: The end date of the search
    :param number_of_tweets: The number of tweets to return
    :return: dataframe of tweets
    """
    tweets_list = []
    current_date = start_date
    while current_date != end_date:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_term + ' since:' + current_date + ' until:' + add_a_day(current_date)).get_items()):
            if i > number_of_tweets:
                break
            tweets_list.append([tweet.user.username, tweet.date, tweet.likeCount, tweet.source, tweet.rawContent])
        current_date = add_a_day(current_date)
    tweets_df = pd.DataFrame(tweets_list, columns=["User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"])
    print(tweets_df.head(10))
        
    return tweets_df

if __name__ == '__main__':
    search_term = input("Enter the search term: ")
    start_date = input("Enter the start date in format Year-Month-Day: ")
    end_date = input("Enter the end date in format Year-Month-Day: ")
    number_of_tweets = int(input("Enter the number of tweets per day: "))
    save_file = input("Enter the name of the file to save the tweets to: ")
    tweets_df = get_tweets(search_term, start_date, end_date, number_of_tweets)
    tweets_df.to_csv(save_file + ".csv", index=False)
    print("Done")







