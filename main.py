import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
import logging
import csv

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


def get_tweets(search_term, start_date, end_date,number_of_tweets, save_file):

    """
    This function will return a list of tweets that match the search term
    :param search_term: The term to search for
    :param start_date: The start date of the search
    :param end_date: The end date of the search
    :param number_of_tweets: The number of tweets to return
    :param save_file: The file to save the tweets to
    :return: None
    """
    current_date = start_date
    try:
        fieldnames = ["User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"]
        with open(save_file + ".csv", "w") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            while current_date != end_date:
                for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_term + ' since:' + current_date + ' until:' + add_a_day(current_date) +' lang:tr').get_items()):
                    if i >= number_of_tweets:
                        break
                    writer.writerow({
                        "User": tweet.user.username,
                        "Date Created": tweet.date,
                        "Number of Likes": tweet.likeCount,
                        "Source of Tweet": tweet.source,
                        "Tweet": tweet.rawContent
                    })
                current_date = add_a_day(current_date)
            logging.info("Scraped tweets and saved to {}.csv".format(save_file))
    except Exception as e:
        logging.error("An error occurred while scraping tweets: {}".format(e))

if __name__ == '__main__':
    logging.basicConfig(filename="scraping.log", level=logging.DEBUG)
    search_term = input("Enter the search term: ")
    start_date = input("Enter the start date in format Year-Month-Day: ")
    end_date = input("Enter the end date in format Year-Month-Day: ")
    number_of_tweets = int(input("Enter the number of tweets per day: "))
    save_file = input("Enter the name of the file to save the tweets to: ")
    get_tweets(search_term, start_date, end_date, number_of_tweets, save_file)
    logging.info("Finished scraping tweets")
