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
