"""
"""

import click
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from rich.table import Column
import yaml


with open("terminology.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

for x in data:
    if x["orgs"] is None:
        x["orgs"] = []


def filter_articles(term: str = None, org: str = None) -> list:
    """"""
    hits = data[:]

    if term:
        hits = [x for x in data if term in x["terms"].keys()]

    if org:
        hits = [x for x in hits if org in x["orgs"]]

    return hits


def filter_terms(hits: list, term: str) -> list:
    """"""
    for hit in hits:
        hit["terms"] = {k: v for k, v in hit["terms"].items() if k == term}

    return hits


def build_results_table(hits: list, sort: str = None):
    """"""

    ## Build the list of results.
    results = []
    for hit in hits:
        for item, definition in hit["terms"].items():
            results.append((
                ", ".join(hit["orgs"]),  # Orgs
                hit["title"],  # Title without link (to be deleted after sorting)
                f"[link={hit['link']}]{hit['title']}[/link]",  # Title with link
                item,
                definition,
            ))

    ## Sort the results according to user's instructions.
    columns = {
        "Orgs": 0,
        "Source": 1,
        "Term": 3
    }
    if sort is not None and sort in columns:
        results = sorted(results, key=lambda x: x[columns[sort]])

    ## Convert the table to a Rich table for console printing.
    table = Table(
        Column("Orgs", style="Magenta", width=20),
        Column("Source", width=40),
        Column("Term", style="Cyan"),
        "Definition",
        title="Results",
        show_lines=True,
    )

    # Remember to only add the title with the link.
    for result in results:
        table.add_row(result[0], result[2], result[3], result[4])

    return table


@click.command()
@click.option("-t", "--term", help="Filter results to a specific term.")
@click.option("-o", "--org", help="Filter results to this organization.")
@click.option("-s", "--sort", help="Which output column to sort by.")
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="If specified, print entire entries instead of condensed table.",
)
def search(
    term: str = None, org: str = None, sort: str = None, verbose: bool = False
) -> dict:
    """Filter articles by a specific term and/or company."""

    hits = filter_articles(term, org)

    if term:
        hits = filter_terms(hits, term)

    if verbose:
        results = hits

    else:
        results = build_results_table(hits, sort)

    console = Console()
    console.print(results)
    return results


if __name__ == "__main__":
    results = search()

    # term = "variant"
    # company = "Amazon"

    # results = filter_by_term(data, term, company)
    # rprint(results)
