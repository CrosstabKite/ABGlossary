"""
TODO
- pretty print the results
    - colors
    - order the dict
    - use tables where possible

- separate the filtering from the results processing
- implement the other questions
- command line
- concise or verbose results
"""

from rich import print as rprint
import yaml


def filter_by_term(data: dict, term: str, company:str = None) -> dict:
    """Filter articles by a specific term.

    Answers questions:
    - What does term W mean?
    - What does company X mean by term W?
    """
    hits = [x for x in data if term in x['terms'].keys()]

    if company:
        hits = [x for x in hits if company in x['orgs']]

    for h in hits:
        h['definition'] = h['terms'][term]
        del h['terms']

    return hits


if __name__ == "__main__":

    with open("terminology.yaml", "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    for x in data:
        if x['orgs'] is None:
            x['orgs'] = []

    term = "variant"
    company = "Amazon"

    results = filter_by_term(data, term, company)
    rprint(results)
