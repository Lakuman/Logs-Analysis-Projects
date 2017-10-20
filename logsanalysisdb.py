#!/usr/bin/python3

import sys
from datetime import date

import psycopg2


def print_info(database_name, queries):

    database, cursor = database_connect(database_name=database_name)
    for idx, query in enumerate(queries):
        print_query(cursor=cursor, query=query)
        print('\n')

    database_disconnect(database=database, cursor=cursor)


def database_connect(database_name):

    database = psycopg2.connect(database=database_name)
    cursor = database.cursor()

    return database, cursor


def database_disconnect(database, cursor):

    if not cursor.closed:
        cursor.close()
    if database.closed != 0:
        database.close()


def fetch_query(cursor, view):

    cursor.execute("SELECT * from " + view)
    posts = cursor.fetchall()
    return posts




def print_query(cursor, query):

    print(query.headline())
    
    results = fetch_query(cursor=cursor, view=query.view)
    for result in results:
        title = result[0]
        value = result[1]

        print("%s -- %s %s" % (title, value, query.suffix))


class Query:

    def __init__(self, question, view, suffix):
        self.question = question
        self.view = view
        self.suffix = suffix

    def headline(self):

        text = "\n %s \n" % self.question
        return text

if __name__ == '__main__':
    DBNAME = "news"
    QUERIES = [
        Query(
            question="What are the most popular three articles of all time?",
            view="pop_articles",
            suffix="views"
        ),
        Query(
            question="Prints the most popular article authors of all time",
            view="pop_authors",
            suffix="views"
        ),
        Query(
            question="On which days did more than 1% of requests " +
            "lead to errors?",
            view="one_percent_errors",
            suffix="% errors"
        )]

    print_info(database_name=DBNAME, queries=QUERIES)

