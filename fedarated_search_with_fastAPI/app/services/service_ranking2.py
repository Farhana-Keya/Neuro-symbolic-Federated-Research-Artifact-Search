from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List


class SearchResult:
    def __init__(self, docid: str, text: str, metadata: Dict, score: float = None):
        self.docid = docid
        self.text = text
        self.metadata = metadata
        self.score = score


class TfidfBasedRanking:
    def __init__(self):
        pass

    def _prepare_documents(self, json_data: Dict) -> List[SearchResult]:
        """
        Prepare documents by merging `description` and `keywords`.
        """

        def extract_keywords(keywords):
            # Handle keywords being a list of strings or dictionaries
            if isinstance(keywords, list):
                extracted = []
                for kw in keywords:
                    if isinstance(kw, str):  # If it's a string, use it directly
                        extracted.append(kw)
                    elif isinstance(kw, dict):  # If it's a dictionary, extract "name" or convert to string
                        extracted.append(kw.get("name", str(kw)))
                return ' '.join(extracted)  # Join all extracted keywords
            return ""  # Return empty string if keywords are not in the expected format

        documents = []
        for item in json_data.get("hits", {}).get("hits", []):
            if '_source' in item and ('description' in item['_source'] or 'keywords' in item['_source']):
                try:
                    merged_text = (
                        f"{item['_source'].get('description', '')} {extract_keywords(item['_source'].get('keywords', []))}"
                    )
                    documents.append(
                        SearchResult(
                            docid=item.get("_id", ""),
                            text=merged_text,
                            metadata=item["_source"]
                        )
                    )
                except Exception as e:
                    print(f"Error processing item {item}: {e}")
        return documents

    def _compute_tfidf_scores(self, query: str, docs: List[SearchResult]) -> List[SearchResult]:
        """
        Compute TF-IDF scores for documents and rank them based on their relevance to the query.
        """
        documents = [doc.text for doc in docs]  # Extract the merged text from documents
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents)

        feature_names = vectorizer.get_feature_names_out()
        if query in feature_names:
            query_idx = vectorizer.vocabulary_[query]
            scores = tfidf_matrix[:, query_idx].toarray().flatten()

            # Assign scores to documents
            for doc, score in zip(docs, scores):
                doc.score = score
        else:
            # Assign a score of 0 if the query is not present
            for doc in docs:
                doc.score = 0

        # Sort documents by their computed scores in descending order
        return sorted(docs, key=lambda x: x.score, reverse=True)

    def _format_ranking_results(self, ranked_results: List[SearchResult]) -> List[Dict]:
        """
        Convert the ranked results into a list of dictionaries including metadata.
        """
        return [
            {
                "docid": result.docid,
                "score": result.score,
                "merged_text": result.text,
                "metadata": result.metadata
            }
            for result in ranked_results
        ]

    def rank_documents(self, json_data: Dict, query: str) -> List[Dict]:
        """
        Rank documents for a query using TF-IDF scoring.

        Parameters:
            json_data (Dict): The JSON data containing documents.
            query (str): The query to rank documents for.

        Returns:
            List[Dict]: Ranked documents with metadata.
        """
        try:
            # print("query ",query)
            # Prepare the documents with merged `description` and `keywords`
            docs = self._prepare_documents(json_data)
            if not docs:
                return []
            # print(f"Prepared Document Text: {docs.text} Metadata: {docs.metadata}")
            # Compute TF-IDF scores and rank documents
            ranked_results = self._compute_tfidf_scores(query, docs)
            # Format the results into a structured JSON format
            response = self._format_ranking_results(ranked_results)
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to rank documents: {str(e)}")
