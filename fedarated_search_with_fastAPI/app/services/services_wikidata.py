import requests
from string import Template
from datetime import datetime
from dateutil import parser
from app.services.find_keyterm_from_question import Keyterm


class MetadataExtractionFromWikidata:
    WIKIDATA_SEARCH_URL = "https://query.wikidata.org/sparql"
    NUMBER_OF_RECORDS = 10  # Limit for search results

    def log_event(self, event_type, message):
        print(f"{event_type.upper()}: {message}")

    class Thing:
        def __init__(self, name="", identifier="", url=""):
            self.name = name
            self.identifier = identifier
            self.url = url

    class Author:
        def __init__(self, name="", identifier=""):
            self.type = "Person"
            self.name = name
            self.identifier = identifier

    class Article:
        def __init__(self):
            self.name = ""
            self.url = ""
            self.identifier = ""
            self.datePublished = ""
            self.author = []
            self.source = []

    def search_wikidata(self, key_term, user_type):
        instance = MetadataExtractionFromWikidata()
        search_results = {}

        print("Key term from wikidata", key_term)
        query_template = self.get_query_template(user_type)

        query = query_template.substitute(search_string=key_term, number_of_records=self.NUMBER_OF_RECORDS)
        response = requests.get(self.WIKIDATA_SEARCH_URL, params={"query": query, "format": "json"})

        if response.status_code != 200:
            instance.log_event("error", f"Failed to fetch data for key term '{key_term}'. Status code: {response.status_code}")
            search_results[key_term] = None
            return search_results

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            instance.log_event("error", f"Failed to decode JSON from response for key term '{key_term}'")
            search_results[key_term] = None
            return search_results

        results = {'publications': [], 'others': []}
        hits = data.get("results", {}).get("bindings", [])
        total_hits = len(hits)
        instance.log_event("info", f"{total_hits} records matched for key term '{key_term}'; pulled top {total_hits}")

        for hit in hits:
            publication = MetadataExtractionFromWikidata.Article()
            publication.name = hit.get("label", {}).get("value", "")
            publication.url = hit.get("item", {}).get("value", "")
            publication.identifier = hit.get("item", {}).get("value", "")

            date_value = hit.get("date", {}).get("value", "")
            if date_value:
                try:
                    publication.datePublished = datetime.strftime(parser.parse(date_value), "%Y-%m-%d")
                except parser.ParserError:
                    instance.log_event("error", f"Invalid date format for item '{publication.name}': {date_value}")
                    publication.datePublished = "Unknown"
            else:
                publication.datePublished = "Unknown"

            authorsLabels = hit.get("authorsLabel", {}).get("value", "")
            for authorsLabel in authorsLabels.rstrip(",").split(","):
                author = MetadataExtractionFromWikidata.Author(name=authorsLabel)
                publication.author.append(author)

            authorsStrings = hit.get("authorsString", {}).get("value", "")
            for authorsString in authorsStrings.rstrip(",").split(","):
                author = MetadataExtractionFromWikidata.Author(name=authorsString)
                publication.author.append(author)

            source = MetadataExtractionFromWikidata.Thing(name="WIKIDATA", url=publication.url)
            publication.source.append(source)

            if publication.identifier:
                results["publications"].append(publication)
            else:
                results["others"].append(publication)

        search_results[key_term] = results
        return search_results

    def get_query_template(self, user_type):
        if user_type == "Dataset":
            return Template('''
                SELECT DISTINCT ?item ?label ?date ?description ?author ?creator ?publisher ?website
                (GROUP_CONCAT(DISTINCT ?authorsName; SEPARATOR=",") AS ?authorsLabel)
                (GROUP_CONCAT(DISTINCT ?authors2; SEPARATOR=",") AS ?authorsString)
                WHERE {
                    SERVICE wikibase:mwapi {
                        bd:serviceParam wikibase:endpoint "www.wikidata.org";
                                        wikibase:limit "once";
                                        wikibase:api "Generator";
                                        mwapi:generator "search";
                                        mwapi:gsrsearch "$search_string";
                                        mwapi:gsrlimit "$number_of_records".
                        ?item wikibase:apiOutputItem mwapi:title.
                    }
                    ?item rdfs:label ?label. FILTER(LANG(?label)="en")
                    VALUES ?type { wd:Q1172284 }
                    ?item wdt:P31 ?type.

                    OPTIONAL { ?item wdt:P577 ?date. }
                    OPTIONAL { ?item wdt:P31 ?instanceOf. }
                    OPTIONAL { ?item wdt:P50 ?author. }
                    OPTIONAL { ?item wdt:P170 ?creator. }
                    OPTIONAL { ?item wdt:P123 ?publisher. }
                    OPTIONAL { ?item wdt:P856 ?website. }
                    OPTIONAL { ?item schema:description ?description. FILTER(LANG(?description) = "en") }
                    OPTIONAL { ?item wdt:P2093 ?authors2. }
                }
                GROUP BY ?item ?label ?date ?description ?author ?creator ?publisher ?website
                LIMIT $number_of_records
            ''')
        else:
            return Template('''
                SELECT DISTINCT ?item ?label ?date ?description ?author ?creator ?publisher ?website
                (GROUP_CONCAT(DISTINCT ?authorsName; SEPARATOR=",") AS ?authorsLabel)
                (GROUP_CONCAT(DISTINCT ?authors2; SEPARATOR=",") AS ?authorsString)
                WHERE {
                    SERVICE wikibase:mwapi {
                        bd:serviceParam wikibase:endpoint "www.wikidata.org";
                                        wikibase:limit "once";
                                        wikibase:api "Generator";
                                        mwapi:generator "search";
                                        mwapi:gsrsearch "$search_string";
                                        mwapi:gsrlimit "$number_of_records".
                        ?item wikibase:apiOutputItem mwapi:title.
                    }
                    ?item rdfs:label ?label. FILTER(LANG(?label)="en")
                    VALUES ?type { wd:Q17155032 wd:Q166142 }
                    ?item wdt:P31 ?type.

                    OPTIONAL { ?item wdt:P577 ?date. }
                    OPTIONAL { ?item wdt:P31 ?instanceOf. }
                    OPTIONAL { ?item wdt:P50 ?author. }
                    OPTIONAL { ?item wdt:P170 ?creator. }
                    OPTIONAL { ?item wdt:P123 ?publisher. }
                    OPTIONAL { ?item wdt:P856 ?website. }
                    OPTIONAL { ?item schema:description ?description. FILTER(LANG(?description) = "en") }
                    OPTIONAL { ?item wdt:P2093 ?authors2. }
                }
                GROUP BY ?item ?label ?date ?description ?author ?creator ?publisher ?website
                LIMIT $number_of_records
            ''')
