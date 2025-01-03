class Unification:
    def __init__(self):
        pass

    def unify_data(self,resodate: dict, wiki: dict) -> dict:
        """
        Unify the resodate and wiki data into a consistent structure.

        Args:
            resodate (dict): Dataset information from resodate.
            wiki (dict): SoftwareApplication data from wiki.

        Returns:
            dict: Unified data structure.
        """
        unified_data = {}

        # Unify resodate
        for category, records in resodate.items():
            unified_data.setdefault(category, {"publications": [], "others": []})
            if not isinstance(records, list):  # Ensure `records` is a list
                print(f"Skipping invalid records in category {category}: {records}")
                continue

            for record in records:
                if not isinstance(record, dict):  # Ensure each record is a dictionary
                    print("type: ",type(record))
                    continue

                metadata = record.get("metadata", {})
                if not isinstance(metadata, dict):  # Ensure `metadata` is a dictionary
                    print(f"Skipping invalid metadata: {metadata}")
                    continue

                unified_data[category]["publications"].append({
                    "name": metadata.get("name", "Unknown"),
                    "url": metadata.get("id", ""),
                    "identifier": record.get("docid", ""),
                    "datePublished": metadata.get("datePublished", "Unknown"),
                    "author": metadata.get("creator", []),
                    "source": [{
                        "name": metadata.get("mainEntityOfPage", [{}])[0].get("provider", {}).get("name", "Unknown")
                        if isinstance(metadata.get("mainEntityOfPage", [{}]), list) else "Unknown",
                        "identifier": metadata.get("mainEntityOfPage", [{}])[0].get("provider", {}).get("id", "")
                        if isinstance(metadata.get("mainEntityOfPage", [{}]), list) else "",
                        "url": metadata.get("mainEntityOfPage", [{}])[0].get("id", "")
                        if isinstance(metadata.get("mainEntityOfPage", [{}]), list) else ""
                    }]
                })

        # Unify wiki
        for category, data in wiki.items():
            unified_data.setdefault(category, {"publications": [], "others": []})
            for publication in data.get("publications", []):
                unified_data[category]["publications"].append({
                    "name": publication.get("name", ""),
                    "url": publication.get("url", ""),
                    "identifier": publication.get("identifier", ""),
                    "datePublished": publication.get("datePublished", "Unknown"),
                    "author": publication.get("author", []),
                    "source": publication.get("source", []),
                    "sources": "wikidata",
                    "Category": category
                })

        return unified_data
