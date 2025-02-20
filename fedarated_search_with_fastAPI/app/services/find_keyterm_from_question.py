import pke
import pandas as pd

class TextRankKeywordsExtraction:
    def __init__(self):
        pass

    def extract_keywords_TextRank(self,question):
        try:
            # Initialize the keyphrase extraction model
            extractor = pke.unsupervised.TextRank()

            # Load the content of the question; preprocessing is done using spaCy
            extractor.load_document(input=question, language='en')

            # Candidate selection (noun and adjective phrases)
            extractor.candidate_selection()

            # Weight the candidates using the TfIdf algorithm
            extractor.candidate_weighting()

            # Get the top 3 keyphrases
            keywords = extractor.get_n_best(n=3)
            print("keywords loop ",type(keywords))

            return [kw[0] for kw in keywords]  # Return only the phrases
        except Exception as e:
            print(f"Error in TextRank extraction: {str(e)}")
            return []
