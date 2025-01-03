from llmrankers.setwise import OpenAiSetwiseLlmRanker
from llmrankers.rankers import SearchResult
from typing import Dict, List


class Ranking_for_resodate:
    def __init__(self):
        pass

    def _check_hits_key(self, json_data: Dict) -> bool:
        """
        Ensure that 'hits' key is present in the input data.
        """
        return 'hits' in json_data

    def _prepare_documents(self, json_data: Dict) -> List[SearchResult]:
        """
        Prepare documents for ranking based on the JSON data.
        """
        # Filter documents by ensuring they have the required metadata
        return [
            SearchResult(
                docid=item['_id'],
                text=f"{item['_source'].get('description', '')} {' '.join(item['_source'].get('keywords', []))} {' '.join(item['_source'].get('name', []))}",
                score=None
            )
            for item in json_data['hits']['hits']
            if '_source' in item and 'description' in item['_source']
        ]

    def _rerank_documents(self, query: str, docs: List[SearchResult], ranker: OpenAiSetwiseLlmRanker) -> List[
        SearchResult]:
        """
        Perform reranking for the current query using the ranker.
        """
        ranked_results = ranker.rerank(query, docs)
        return sorted(ranked_results, key=lambda x: x.score, reverse=True)

    def _format_ranking_results(self, ranked_results: List[SearchResult], json_data: Dict) -> List[Dict]:
        """
        Convert the reranked results into JSON format with full metadata.
        """
        # Optimize lookups by indexing documents by their IDs
        id_to_doc = {item['_id']: item for item in json_data['hits']['hits']}

        ranked_json = []
        for result in ranked_results:
            doc = id_to_doc.get(result.docid, {})
            ranked_json.append({
                'docid': result.docid,
                # 'score': result.score,
                'metadata': doc.get('_source', {})  # Include full metadata
            })
        return ranked_json

    def rank_documents_for_queries(self, json_data: Dict, queries: List[str]) -> Dict[str, List[Dict]]:
        """
        Rank documents for multiple queries using a setwise ranker.

        Parameters:
            json_data (Dict): The JSON data containing documents.
            queries (List[str]): A list of queries.

        Returns:
            Dict[str, List[Dict]]: A dictionary where each query maps to ranked documents with metadata.
        """
        print("ranking for resodate ")
        # print(" jsondata ",json_data)
        # print("queries ",queries)
        try:
            # Step 1: Ensure that 'hits' key is present in the input data
            # if not self._check_hits_key(json_data):
            #     raise ValueError("'hits' key is missing in the provided json_data")
            # Step 2: Initialize the Setwise LLM Ranker
            ranker = OpenAiSetwiseLlmRanker(
                model_name_or_path="gpt-3.5-turbo",
                api_key= "sk-lUeE-816Y8nMtTAWipqykGqPogHCbEG3DQKD7DvuYkT3BlbkFJTLw6nP_-G0j_gxugKCxe2Uz6yQ1nVysyNK5K6QM4kA",  # Replace with environment variable for better security
                num_child=2,
                method="heapsort",
                k=10
            )

            # Step 3: Rank documents for each query
            results = {}
            data_dict = {}

            for query in queries:
                hpd_data = None
                # for key, value in json_data.items():
                #     print("key ",key)
                #     print("value ",value)
                #     if isinstance(value, dict) and query in value:
                #         hpd_data = value[query]
                #         break
                for key, value in json_data.items():
                    # print("key ",key)
                    # print("value ",value)
                    if isinstance(value, dict) and query == key:
                        data_dict[query] = value


                # If no data found, set it as empty
                # data_dict[query] = hpd_data or {}
                # print("data dict resodate ", data_dict)
            for query in queries:
                data= data_dict[query]
                if self._check_hits_key(data):
                        # Prepare documents for ranking



                        docs = self._prepare_documents(data)
                        # print("docs ",docs)

                        if docs:  # Only rerank if there are documents
                            # Perform reranking for the matched documents
                            ranked_results = self._rerank_documents(query, docs, ranker)

                            # Format the reranked results with full metadata
                            ranked_json = self._format_ranking_results(ranked_results, data)

                            # Store the ranked results for this query
                            results[query] = ranked_json
                        else:
                            results[query] = []
                else:
                        # If no documents match the query, store an empty result
                        results[query] = []

            return results

        except Exception as e:
            raise RuntimeError(f"Failed to rerank documents: {str(e)}")
# class Ranking_for_wikidata:
#     def __init__(self):
#         pass
#
#     def _prepare_documents(self, json_data: Dict) -> List[SearchResult]:
#         """
#         Prepare documents for ranking based on the 'name' field, and assign scores.
#         """
#         results = []
#
#         # Iterate through categories in the JSON
#         for category, data in json_data.get("wikidata with SoftwareApplication", {}).items():
#
#             # Extract publications within each category
#             for publication in data.get("publications", []):
#                 results.append(
#                     SearchResult(
#                         docid=publication.get("identifier", ""),
#                         text=publication.get("name", ""),  # Use `name` for ranking
#                         score=0.0  # Default score to allow the ranker to process
#                     )
#                 )
#
#         return results
#
#     def _rerank_documents(self, query: str, docs: List[SearchResult], ranker: OpenAiSetwiseLlmRanker) -> List[SearchResult]:
#         """
#         Perform reranking for the current query using the ranker.
#         """
#         ranked_results = ranker.rerank(query, docs)
#         # Sort the results by score in descending order
#         return sorted(ranked_results, key=lambda x: x.score, reverse=True)
#
#     def _format_ranking_results(self, ranked_results: List[SearchResult], json_data: Dict) -> List[Dict]:
#         """
#         Convert the reranked results into JSON format with full metadata.
#         """
#         id_to_metadata = {}
#         for category, data in json_data.items():
#             for publication in data.get("publications", []):
#                 id_to_metadata[publication.get("identifier", "")] = publication
#
#         ranked_json = []
#         for result in ranked_results:
#             metadata = id_to_metadata.get(result.docid, {})
#             ranked_json.append({
#                 'docid': result.docid,
#                 'score': result.score,
#                 'metadata': metadata
#             })
#         return ranked_json
#
#     def _is_effectively_empty(self, data: dict) -> bool:
#         """
#         Check if a dictionary is effectively empty (all its values are empty).
#         """
#         return all(not value for value in data.values())
#
#     def rank_documents_for_queries(self, json_data: Dict, queries: List[str]) -> Dict[str, List[Dict]]:
#         """
#         Rank documents for multiple queries using a setwise ranker.
#
#         Parameters:
#             json_data (Dict): The JSON data containing documents.
#             queries (List[str]): A list of queries.
#
#         Returns:
#             Dict[str, List[Dict]]: A dictionary where each query maps to ranked documents with metadata.
#         """
#         print("json data ",json_data)
#         try:
#             ranker = OpenAiSetwiseLlmRanker(
#                 model_name_or_path="gpt-3.5-turbo",
#                 api_key="sk-lUeE-816Y8nMtTAWipqykGqPogHCbEG3DQKD7DvuYkT3BlbkFJTLw6nP_-G0j_gxugKCxe2Uz6yQ1nVysyNK5K6QM4kA",  # Replace with a secure method
#                 num_child=2,
#                 method="heapsort",
#                 k=10
#             )
#             results = {}
#             data_dict = {}
#             for query in queries:
#                 # data_dict[query] = {}  # Initialize empty data for each query
#
#                 # Collect the data for each query
#                 for key, value in json_data.items():
#                     print("key ", key)
#                     print("value ", value)
#                     if query.lower() in key.lower():  # Match query with category
#                         data_dict[query] = value
#
#
#             # Process each query
#             for query in queries:
#                 # data_dict[query] = {}  # Initialize empty data for each query
#                 #
#                 # # Collect the data for each query
#                 # for key, value in json_data.items():
#                 #     print("key ",key)
#                 #     print("value ",value)
#                 #     if query.lower() in key.lower():  # Match query with category
#                 #         data_dict[query] = value
#
#                 # Process the data for each query
#                 data = data_dict[query]
#
#                 if self._is_effectively_empty(data):
#                     results[query] = []  # No documents to rank for this query
#                 else:
#                     docs = self._prepare_documents(data)
#                     if docs:
#                         ranked_results = self._rerank_documents(query, docs, ranker)
#                         ranked_json = self._format_ranking_results(ranked_results, json_data)
#                         results[query] = ranked_json
#                     else:
#                         results[query] = []  # No documents to rank for this query
#
#             return results
#
#         except Exception as e:
#             raise RuntimeError(f"Failed to rerank documents: {str(e)}")
#


class Ranking_for_wikidata:
    def __init__(self):
        pass

    def _prepare_documents(self, json_data: Dict) -> List[SearchResult]:
        """
        Prepare documents for ranking based on the 'name' field, and assign scores.
        """
        results = []

        # Iterate through categories in the JSON
        for category, data in json_data.get("wikidata with SoftwareApplication", {}).items():

            # Extract publications within each category
            for publication in data.get("publications", []):
                # Ensure each publication is serialized to a dictionary if it is an object
                if hasattr(publication, 'to_dict'):
                    publication_data = publication.to_dict()  # Convert Article object to dict
                else:
                    publication_data = publication  # Already a dictionary

                results.append(
                    SearchResult(
                        docid=publication_data.get("identifier", ""),
                        text=publication_data.get("name", ""),  # Use `name` for ranking
                        score=0.0  # Default score to allow the ranker to process
                    )
                )

        return results

    def _rerank_documents(self, query: str, docs: List[SearchResult], ranker: OpenAiSetwiseLlmRanker) -> List[SearchResult]:
        """
        Perform reranking for the current query using the ranker.
        """
        ranked_results = ranker.rerank(query, docs)
        # Sort the results by score in descending order
        return sorted(ranked_results, key=lambda x: x.score, reverse=True)

    def _format_ranking_results(self, ranked_results: List[SearchResult], json_data: Dict) -> List[Dict]:
        """
        Convert the reranked results into JSON format with full metadata.
        """
        id_to_metadata = {}
        for category, data in json_data.items():
            for publication in data.get("publications", []):
                id_to_metadata[publication.get("identifier", "")] = publication

        ranked_json = []
        for result in ranked_results:
            metadata = id_to_metadata.get(result.docid, {})
            ranked_json.append({
                'docid': result.docid,
                'score': result.score,
                'metadata': metadata
            })
        return ranked_json

    def _is_effectively_empty(self, data: dict) -> bool:
        """
        Check if a dictionary is effectively empty (all its values are empty).
        """
        return all(not value for value in data.values())

    def rank_documents_for_queries(self, json_data: Dict, queries: List[str]) -> Dict[str, List[Dict]]:
        """
        Rank documents for multiple queries using a setwise ranker.

        Parameters:
            json_data (Dict): The JSON data containing documents.
            queries (List[str]): A list of queries.

        Returns:
            Dict[str, List[Dict]]: A dictionary where each query maps to ranked documents with metadata.
        """
        print("json data ", json_data)
        try:
            ranker = OpenAiSetwiseLlmRanker(
                model_name_or_path="gpt-3.5-turbo",
                api_key="sk-lUeE-816Y8nMtTAWipqykGqPogHCbEG3DQKD7DvuYkT3BlbkFJTLw6nP_-G0j_gxugKCxe2Uz6yQ1nVysyNK5K6QM4kA",  # Replace with a secure method
                num_child=2,
                method="heapsort",
                k=10
            )
            results = {}
            data_dict = {}
            for query in queries:
                # Collect the data for each query
                for key, value in json_data.items():
                    # print("key ", key)
                    # print("value ", value)
                    if query.lower() in key.lower():  # Match query with category
                        data_dict[query] = value

            # Process each query
            for query in queries:
                data = data_dict.get(query, {})

                if self._is_effectively_empty(data):
                    results[query] = []  # No documents to rank for this query
                else:
                    docs = self._prepare_documents(data)
                    if docs:
                        ranked_results = self._rerank_documents(query, docs, ranker)
                        ranked_json = self._format_ranking_results(ranked_results, json_data)
                        results[query] = ranked_json
                    else:
                        results[query] = []  # No documents to rank for this query

            return results

        except Exception as e:
            raise RuntimeError(f"Failed to rerank documents: {str(e)}")


