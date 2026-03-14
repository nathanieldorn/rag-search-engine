#!/usr/bin/env python3

import argparse
import json
import string

from nltk.stem import PorterStemmer


def read_json() -> dict:
    """Reads the json movies file and returns it as a dictionary"""
    with open("data/movies.json", "r") as file:
        movies_dict = json.load(file)
    return movies_dict


def read_stopwords() -> list:
    """Reads the txt file of words to remove from query results"""
    with open("data/stopwords.txt", "r") as file:
        stopwords_string = file.read()
        stopwords_list = stopwords_string.splitlines()
    return stopwords_list


def tokenize_strings(string: str) -> list:
    """Break strings into a list of single word tokens, conver to lowercase, and remove stopwords"""
    split_string = string.split()
    stemmer = PorterStemmer()
    # create token list as a list comprehension
    token_list = [
        stemmer.stem(token.lower())
        for token in split_string
        if token != "" and token not in read_stopwords()
    ]

    """
    # create token list with a for loop
    token_list = []
    for i in range(len(split_string)):
        if split_string[i] == "":
            continue
        token_list.append(split_string[i])
    """
    return token_list


def search_movies(movies_dict: dict, query: str) -> list:
    """Returns a list of movie titles from the json that contain the query string"""
    # create a table to remove all punctation from query and title strings
    translation_table = str.maketrans("", "", string.punctuation)
    clean_query = query.translate(translation_table)
    # split_query = clean_query.split()

    # using tokens
    split_query = tokenize_strings(clean_query)

    # find results as a list comprehension, remove comments to use
    search_results = [
        # movie["title"]
        # for movie in movies_dict["movies"]
        # if clean_query in movie["title"].translate(translation_table).lower()
    ]

    # find results as a for loop
    for i in range(len(movies_dict["movies"])):
        title_tokens = tokenize_strings(movies_dict["movies"][i]["title"])
        for j in range(len(split_query)):
            for k in range(len(title_tokens)):
                if split_query[j] in title_tokens[k]:
                    if movies_dict["movies"][i]["title"] in search_results:
                        continue
                    else:
                        search_results.append(movies_dict["movies"][i]["title"])

    return search_results


def print_results(results: list, limit: int) -> None:
    """Prints the results of a query to a defined limit"""
    x, i = 1, 0
    if not results:
        print("Nothing found.")
    while i < len(results) and i < limit:
        print(f"{x}. {results[i]}")
        x += 1
        i += 1
    if limit < len(results):
        print("...")


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            # print the search query here
            print(f"Searching for: {args.query}")
            print_results(search_movies(read_json(), args.query), 5)

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
