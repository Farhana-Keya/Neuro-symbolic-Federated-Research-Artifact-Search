import requests
import json
import sys
import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.services.find_keyterm_from_question import Keyterm
import re
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from rake_nltk import Rake
import yake


class MetadataExtractionFromResodate:
    API_URL = "https://resodate.org/resources/api/search/_search?pretty"

    def __init__(self):
        # self.keyterm_extractor = Keyterm()
        pass

    def search_resodate_data(self, key_term, user_type):
        """
        Extracts key terms from the question, queries the Resodate API,
        and stores results for each key term in a dictionary.
        """
        # Step 1: Extract key terms from the question
        # key_terms = self.keyterm_extractor.extract_key_term(question)
        # print("user type ",user_type)
        # content_type = user_type.split("Choice=")[1]
        # print(" content type ",content_type)
        search_results = {}
        data={}

        # Step 2: Query the Resodate API for each key term

        query = self._build_query(key_term, user_type)
        response = requests.post(self.API_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(query))

        if response.status_code == 200:
            data = self._clean_response_data(response.json())
            # search_results[key_term] = data
        else:
            print(f"API request failed for term '{key_term}' with status code {response.status_code}")

        return data
    # def search_resodate_data(self, question, user_type):
    #     """
    #     Extracts key terms from the question, queries the Resodate API,
    #     and stores results for each key term and user type in a dictionary.
    #     """
    #     # Step 1: Extract key terms from the question
    #     key_terms = self.keyterm_extractor.extract_key_term(question)
    #     print("User types: ", user_type)
    #
    #     # Ensure `user_type` is a list
    #     if isinstance(user_type, str):
    #         user_type = [user_type]
    #
    #     search_results = {}
    #
    #     # Step 2: Query the Resodate API for each key term and user type
    #     for term in key_terms:
    #         search_results[term] = {}
    #         for content_type in user_type:  # Iterate over user types
    #             # Build query for the current term and content type
    #             query = self._build_query(term, content_type)
    #
    #             # Query the API
    #             response = requests.post(self.API_URL, headers={'Content-Type': 'application/json'},
    #                                      data=json.dumps(query))
    #
    #             # Handle the API response
    #             if response.status_code == 200:
    #                 data = self._clean_response_data(response.json())
    #                 search_results[term][content_type] = data
    #             else:
    #                 print(
    #                     f"API request failed for term '{term}' and content type '{content_type}' with status code {response.status_code}")
    #                 search_results[term][content_type] = {}
    #
    #     return search_results

    def _build_query(self, key_term, content_type):
        """Builds a query payload for the Resodate API based on the key term and content type."""
        return {
            "size": 20,
            "from": 0,
            "query": {
                "bool": {
                    "must": [
                        {"multi_match": {"query": key_term, "fields": ["name", "description", "keywords"]}},
                        {"term": {"type": content_type}}
                    ]
                }
            }
        }

    # def _clean_response_data(self, data):
    #     """Cleans the API response data by removing unnecessary keys."""
    #     keys_to_remove = ["took", "timed_out", "_shards", "max_score", "_index", "_type", "_id","_score","relation"]
    #     for key in keys_to_remove:
    #         data.pop(key, None)
    #     return data
    def _clean_response_data(self, data):
        """Cleans the API response data by removing unnecessary keys."""
        keys_to_remove = ["took", "timed_out", "_shards", "max_score", "_index", "_type", "_score", "relation"]

        # Remove top-level keys
        for key in keys_to_remove:
            data.pop(key, None)

        # Clean nested keys inside hits["hits"]
        if "hits" in data and "hits" in data["hits"]:
            for hit in data["hits"]["hits"]:
                for key in keys_to_remove:
                    hit.pop(key, None)

        return data
