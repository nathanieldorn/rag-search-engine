#!/usr/bin/env python3

import argparse
import json


def read_json() -> dict:
    """Reads the json movies file and returns it as a dictionary"""
    with open("data/movies.json", "r") as file:
        movies_dict = json.load(file)
    return movies_dict


def search_movies(movies_dict: dict, query: str) -> list:
    """Returns a list of movie titles from the json that contain the query string"""
    # as a list comprehension
    search_results = [
        movie["title"] for movie in movies_dict["movies"] if query in movie["title"]
    ]
    """
    # as a for loop
    for i in range(len(movies_dict["movies"])):
        if query in movies_dict["movies"][i]["title"]:
            search_results.append(movies_dict["movies"][i]["title"])
    """
    return search_results


def print_results(results: list, limit: int) -> None:
    """Prints the results of a query to a defined limit"""
    x, i = 1, 0
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
