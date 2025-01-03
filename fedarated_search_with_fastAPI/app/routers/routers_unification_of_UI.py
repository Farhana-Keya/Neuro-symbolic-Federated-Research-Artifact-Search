# # import sys
# #
# # sys.path.append("..")
# # from fastapi import APIRouter, HTTPException, Depends
# # from pydantic import BaseModel
# # from typing import Literal, Dict, Any
# # from app.common.util.decorators import log
# # from app.services.services_resodate import MetadataExtractionFromResodate
# # from app.services.services_wikidata import MetadataExtractionFromWikidata
# #
# # router = APIRouter()
# #
# # # Models for input validation
# # class QuestionRequest(BaseModel):
# #     question: str
# #
# # class Quiz(BaseModel):
# #     server: Literal['*', 'resodate', 'wikidata']  # Dropdown for server
# #     resource_type: Literal['*', 'Dataset', 'SoftwareApplication']  # Dropdown for resource type
# #
# # # Function to query Resodate API
# # def query_resodate(question: str, resource_type: str):
# #     try:
# #         resodate_metadata = MetadataExtractionFromResodate()
# #         return resodate_metadata.search_resodate_data(question, resource_type)
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"Resodate API error: {str(e)}")
# #
# # # Function to query Wikidata API
# # def query_wikidata(question: str, resource_type: str):
# #     try:
# #         wikidata_metadata = MetadataExtractionFromWikidata()
# #         return wikidata_metadata.search_wikidata(question, resource_type)
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"Wikidata API error: {str(e)}")
# #
# # # Function to handle resource_type queries
# # def handle_resource_type(question: str, resource_type: str, server: str) -> Dict[str, Any]:
# #     responses = {}
# #
# #     # If resource_type is '*', query both types
# #     resource_types = ['Dataset', 'SoftwareApplication'] if resource_type == '*' else [resource_type]
# #
# #     for r_type in resource_types:
# #         if server in ('*', 'resodate'):
# #             responses[f"**resodate with {r_type}**\n\n"] = query_resodate(question, r_type)
# #         if server in ('*', 'wikidata'):
# #             responses[f"**wikidata with {r_type}**\n\n"] = query_wikidata(question, r_type)
# #
# #     return responses
# #
# # # Main function for handling the request
# # @router.post('/question', status_code=200)
# # @log(__name__)
# # def search_question(Question, type_info: Quiz = Depends()):
# #     """
# #     Dynamically query based on user input:
# #     - `server`: Selects which API(s) to query ('*', 'resodate', 'wikidata').
# #     - `resource_type`: Selects the resource type ('*', 'Dataset', 'SoftwareApplication').
# #     """
# #     question = str(Question)
# #     server = type_info.server
# #     resource_type = type_info.resource_type
# #
# #     try:
# #         # Delegate to the resource_type handler
# #         responses = handle_resource_type(question, resource_type, server)
# #
# #         # Return results
# #         return {"status": "success", "data": responses}
# #     except HTTPException as http_exc:
# #         # Re-raise HTTPExceptions for FastAPI to handle
# #         raise http_exc
# #     except Exception as e:
# #         # Handle unexpected errors
# #         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
#
#
# import sys
#
# sys.path.append("..")
# from fastapi import APIRouter, HTTPException, Depends
# from pydantic import BaseModel
# from typing import Literal, Dict, Any
# from app.common.util.decorators import log
# from app.services.services_resodate import MetadataExtractionFromResodate
# from app.services.services_wikidata import MetadataExtractionFromWikidata
# from app.services.find_keyterm_from_question import Keyterm
# from app.services.service_ranking  import Ranking_for_resodate, Ranking_for_wikidata
# from app.services.service_unification_data import Unification
# from app.services.service_ranking2 import TfidfBasedRanking
#
# router = APIRouter()
#
#
# # Models for input validation
# class QuestionRequest(BaseModel):
#     question: str
#
#
# class Quiz(BaseModel):
#     server: Literal['*', 'resodate', 'wikidata']  # Dropdown for server
#     resource_type: Literal['*', 'Dataset', 'SoftwareApplication']  # Dropdown for resource type
#     # ranking_method: Literal['default', 'custom']  # Dropdown for ranking method
#
#
# # Function to query Resodate API
# def query_resodate(question: str, resource_type: str):
#     try:
#         resodate_metadata = MetadataExtractionFromResodate()
#         return resodate_metadata.search_resodate_data(question, resource_type)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Resodate API error: {str(e)}")
#
#
# # Function to query Wikidata API
# def query_wikidata(question: str, resource_type: str):
#     try:
#         wikidata_metadata = MetadataExtractionFromWikidata()
#         return wikidata_metadata.search_wikidata(question, resource_type)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Wikidata API error: {str(e)}")
#
#
# # Function to rank metadata
# # def rank_metadata(metadata: Dict[str, Any], ranking_method: str) -> Dict[str, Any]:
# #     if ranking_method == "custom":
# #         # Implement custom ranking logic here
# #         sorted_metadata = {k: v for k, v in sorted(metadata.items(), key=lambda item: len(item[1]), reverse=True)}
# #     else:
# #         # Default ranking method: simple alphabetic sorting by key
# #         sorted_metadata = {k: v for k, v in sorted(metadata.items(), key=lambda item: item[0])}
# #
# #     return sorted_metadata
#
#
# # Function to handle resource_type queries
# # def handle_resource_type(question: str, resource_type: str, server: str,key_terms:list) -> Dict[str, Any]:
# #     responses = {}
# #     rank_response={}
# #     # ranking_ob = Ranking()
# #
# #
# #     # If resource_type is '*', query both types
# #     resource_types = ['Dataset', 'SoftwareApplication'] if resource_type == '*' else [resource_type]
# #
# #     for r_type in resource_types:
# #         if server in ('*', 'resodate'):
# #             responses[f"resodate with {r_type}"] = query_resodate(question, r_type)
# #             rank_response["resodate with {r_type}"]=
# #         if server in ('*', 'wikidata'):
# #             responses[f"wikidata with {r_type}"] = query_wikidata(question, r_type)
# #         # if server =='resodate':
# #         #     responses[f"resodate"] = query_resodate(question, r_type)
# #         # elif server =='wikidata':
# #         #     responses[f"wikidata"] = query_wikidata(question, r_type)
# #         # elif server == '*':
# #         #     responses[f"resodate,wikidata"] = query_resodate(question, r_type).update(query_wikidata(question, r_type))
# #
# #
# #
# #     # Rank metadata based on selected ranking method
# #     return responses
#
#
# def handle_resource_type(question: str, resource_type: str, server: str, key_terms: list) -> Dict[str, Any]:
#     responses = {}
#     rank_response = {}
#
#     # Initialize ranking objects
#     # resodate_ranker = Ranking_for_resodate()
#     # wikidata_ranker = Ranking_for_wikidata()
#     resodate_ranker = TfidfBasedRanking()
#
#     # If resource_type is '*', query both types
#     resource_types = ['Dataset', 'SoftwareApplication'] if resource_type == '*' else [resource_type]
#
#     for r_type in resource_types:
#         if server in ('*', 'resodate'):
#             # Query resodate and rank the responses
#             raw_resodate_response = query_resodate(question, r_type)
#             ranked_resodate = resodate_ranker.rank_documents(raw_resodate_response, key_terms)
#             responses[f"resodate with {r_type}"] = raw_resodate_response
#             rank_response[f"ranked resodate with {r_type}"] = ranked_resodate
#
#         if server in ('*', 'wikidata'):
#             # Query wikidata and rank the responses
#             raw_wikidata_response = query_wikidata(question, r_type)
#             # ranked_wikidata = wikidata_ranker.rank_documents_for_queries(raw_wikidata_response, key_terms)
#             responses[f"wikidata with {r_type}"] = raw_wikidata_response
#             # rank_response[f"ranked wikidata with {r_type}"] = ranked_wikidata
#
#     return responses, rank_response
#
#
# # Main function for handling the request
# @router.post('/question', status_code=200)
# @log(__name__)
# def search_question(Question, type_info: Quiz = Depends()):
#     """
#     Dynamically query based on user input:
#     - `server`: Selects which API(s) to query ('*', 'resodate', 'wikidata').
#     - `resource_type`: Selects the resource type ('*', 'Dataset', 'SoftwareApplication').
#     """
#     question = str(Question)
#     keywords = Keyterm()
#     get_keywords = keywords.extract_key_term(question)
#     server = type_info.server
#     resource_type = type_info.resource_type
#     # ranking_method = type_info.ranking_method
#     # ranking_ob = Ranking()
#     unify=Unification()
#
#     try:
#         # Delegate to the resource_type handler
#         responses, ranked_responses  = handle_resource_type(question, resource_type, server,get_keywords)
#         # ranked_response = ranking_ob.rank_documents_for_queries(responses,get_keywords)
#
#         # Return results
#         unified_data = unify.unify_data(ranked_responses,responses)
#         print("response ",responses)
#         # return {"status": "success", "Unification":unified_data}
#         return {"status": "success", "data": responses}
#
#
#
#     except Exception as e:
#         # Handle unexpected errors
#         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


from fastapi import APIRouter, HTTPException, Depends
from ipykernel.datapub import publish_data
from pydantic import BaseModel
from typing import Literal, Dict, Any, List
from app.common.util.decorators import log
from app.services.services_resodate import MetadataExtractionFromResodate
from app.services.services_wikidata import MetadataExtractionFromWikidata
from app.services.find_keyterm_from_question import Keyterm
from app.services.service_ranking2 import TfidfBasedRanking
from app.services.service_unification_data import Unification

router = APIRouter()


# Models for input validation
class QuestionRequest(BaseModel):
    question: str


class Quiz(BaseModel):
    server: Literal['*', 'resodate', 'wikidata']  # Dropdown for server
    resource_type: Literal['*', 'Dataset', 'SoftwareApplication']  # Dropdown for resource type


# Function to query Resodate API
def query_resodate(question: str, resource_type: str):
    try:
        resodate_metadata = MetadataExtractionFromResodate()
        return resodate_metadata.search_resodate_data(question, resource_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resodate API error: {str(e)}")


# Function to query Wikidata API
def query_wikidata(question: str, resource_type: str):
    try:
        wikidata_metadata = MetadataExtractionFromWikidata()
        return wikidata_metadata.search_wikidata(question, resource_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Wikidata API error: {str(e)}")


# Function to process metadata and rank for keywords
def process_metadata_and_rank_for_keywords(
        question: str, key_terms: List[str], resource_type: str, server: str
) -> Dict[str, List[Dict]]:
    responses = []
    resodate_ranker = TfidfBasedRanking()

    for keyword in key_terms:
        keyword_responses = {"keyword": keyword, "results": []}

        for r_type in (['Dataset', 'SoftwareApplication'] if resource_type == '*' else [resource_type]):
            if server == '*':
                resodate_response = query_resodate(keyword, r_type)
                ranked_resodate = resodate_ranker.rank_documents(resodate_response, keyword)
                print("ranked_resodate ", ranked_resodate)
                keyword_responses["results"].append({"source": "resodate", "ranked": ranked_resodate})

                wikidata_response = query_wikidata(keyword, r_type)
                ranked_wikidata = resodate_ranker.rank_documents(wikidata_response, keyword)
                keyword_responses["results"].append({"source": "wikidata", "ranked": ranked_wikidata})

            elif server == 'resodate':
                resodate_response = query_resodate(keyword, r_type)
                ranked_resodate = resodate_ranker.rank_documents(resodate_response, keyword)
                print("ranked_resodate ",ranked_resodate)
                keyword_responses["results"].append({"source": "resodate", "ranked": ranked_resodate})

            elif server == 'wikidata':
                wikidata_response = query_wikidata(keyword, r_type)
                ranked_wikidata = resodate_ranker.rank_documents(wikidata_response, keyword)
                keyword_responses["results"].append({"source": "wikidata", "ranked": ranked_wikidata})

        responses.append(keyword_responses)

    return {"responses": responses, "server": server}


# Unify and format results
def unify_and_format_results(data: Dict) -> List[Dict]:
    unified_results = []
    unification = Unification()

    def extract_names(data):
        # Ensure the list contains strings
        if isinstance(data, list):
            return [d if isinstance(d, str) else d.get("name", "") for d in data]
        return []

    responses = data["responses"]

    for keyword_response in responses:
        keyword = keyword_response["keyword"]
        for result_group in keyword_response["results"]:
            source = result_group["source"]  # This will be either 'resodate' or 'wikidata'
            ranked_results = result_group["ranked"]

            for result in ranked_results:
                metadata = result.get("metadata", {})

                # Ensure metadata is a dictionary before calling get()
                if isinstance(metadata, dict):
                    description = metadata.get("description", "")
                    language = metadata.get("inLanguage", "N/A")
                    resource_type = metadata.get("type", "N/A")
                    institutions = ", ".join(extract_names(metadata.get("institutions", [])))
                    persons = ", ".join(extract_names(metadata.get("persons", [])))
                    keywords = ", ".join(extract_names(metadata.get("keywords", [])))  # Extract keywords from metadata
                else:
                    description = ""
                    language = "N/A"
                    resource_type = "N/A"
                    institutions = ""
                    persons = ""
                    keywords = ""  # Default to empty if no keywords

                formatted_result = {
                    "Keyterm": keyword,
                    "Keywords": keywords,  # Keywords from metadata added here
                    "Description": description,
                    "Language": language,
                    "ResourceType": resource_type,
                    "Institution": institutions,
                    "Persons": persons,
                    "Source": source
                }

                # Directly append formatted results to unified_results
                unified_results.append(formatted_result)

    # Return unified results directly instead of passing the same list
    return unified_results




# Main function for handling the request
@router.post('/question', status_code=200)
@log(__name__)
def search_question(Question, type_info: Quiz = Depends()):
    """
    Dynamically query based on user input:
    - `server`: Selects which API(s) to query ('*', 'resodate', 'wikidata').
    - `resource_type`: Selects the resource type ('*', 'Dataset', 'SoftwareApplication').
    """
    question = str(Question)
    keyterm_extractor = Keyterm()
    key_terms = keyterm_extractor.extract_key_term(question)
    server = type_info.server
    resource_type = type_info.resource_type

    try:
        # Process metadata for each keyword individually
        ranked_responses = process_metadata_and_rank_for_keywords(question, key_terms, resource_type, server)
        print("ranked_responses ",ranked_responses)
        # Unify and format results for each keyword
        unified_results = unify_and_format_results(ranked_responses)

        return {"status": "success", "data": unified_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
