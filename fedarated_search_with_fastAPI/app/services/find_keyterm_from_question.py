import openai

# api_key="sk-lUeE-816Y8nMtTAWipqykGqPogHCbEG3DQKD7DvuYkT3BlbkFJTLw6nP_-G0j_gxugKCxe2Uz6yQ1nVysyNK5K6QM4kA",
class Keyterm:
    def __init__(self):
        pass

    openai.api_key = 'sk-lUeE-816Y8nMtTAWipqykGqPogHCbEG3DQKD7DvuYkT3BlbkFJTLw6nP_-G0j_gxugKCxe2Uz6yQ1nVysyNK5K6QM4kA'
    def extract_key_term(self, question):
        prompt = f"""
                Extract the main key topics or subjects from the following question, focusing on essential nouns and named entities. 
                Avoid generic terms such as 'impact', 'effect', 'role' or dashes ('-') or any unnecessary characters in the output. 
                

                Question: "{question}"

                Key topics:
                """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant that extracts key topics from text, focusing on main subjects and excluding general terms like 'impact' or 'effect'."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.3,
            n=1,
            stop=["\n"]
        )

        # Extract the key phrases from the response
        key_terms = response['choices'][0]['message']['content'].strip().split(", ")
        # print("key_terms from openai ", key_terms)
        return key_terms